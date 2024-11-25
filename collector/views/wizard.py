import base64

from django.forms import BaseFormSet
from formtools.wizard.views import SessionWizardView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from collector.models import Observation, Species, ObservationSpecies, Plot
from collector.forms import ObservationLocationPhotoForm, ObservationPlotForm, ObservationMeasurementForm, ObservationSpeciesFormSet



class ObservationSuccessView(TemplateView):
    template_name = 'collector/wizard/success.html'


TEMPLATES = {"locphoto": 'collector/wizard/loc_photo.html',
             "plot": 'collector/wizard/plot.html',
             "measure": 'collector/wizard/measurements.html',
             "species": 'collector/wizard/species.html'}

class ObservationWizard(LoginRequiredMixin, SessionWizardView):
    form_list = [("locphoto", ObservationLocationPhotoForm),
                 ("plot", ObservationPlotForm),
                 ("measure", ObservationMeasurementForm),
                 ("species", ObservationSpeciesFormSet)]

    def get_form(self, step=None, data=None, files=None):
        """
        Override to handle formset for 'species' step.
        """
        step = step or self.steps.current
        if step == "species":
            if data:
                return ObservationSpeciesFormSet(data=data)
            else:
                return ObservationSpeciesFormSet()
        return super().get_form(step, data, files)

    def post(self, *args, **kwargs):
        """
        Override the post method to handle 'Back' button clicks.
        """
        if 'wizard_goto_step' in self.request.POST:
            goto_step = self.request.POST.get('wizard_goto_step')

            # Get the current form and process its data to save it
            current_form = self.get_form(data=self.request.POST)
            if current_form.is_valid() or current_form.data:
                self.process_step(current_form)

            self.storage.current_step = goto_step
            #print(f"Going back to step {goto_step}")
            return self.render_goto_step(goto_step)

        return super().post(*args, **kwargs)

    def process_step(self, form):
        """
        Save formset data for the 'species' step.
        """
        if self.steps.current == "species" and isinstance(BaseFormSet, ObservationSpeciesFormSet):
            step_data = {
                f"form-{i}-{key}": value
                for i, form_data in enumerate(form.cleaned_data)
                if form_data
                for key, value in form_data.items()
            }
            self.storage.set_step_data(self.steps.current, step_data)
        else:
            step_data = form.data  # Use form.data to ensure even incomplete data is saved
            #print(f"Saving data for step {self.steps.current}: {step_data}")
            self.storage.set_step_data(self.steps.current, step_data)

        return super().process_step(form)

    def get_form_initial(self, step):
        """
        Load previously saved data into the form fields when revisiting a step.
        """
        step_data = self.storage.get_step_data(step)
        #print(f"Loading data for step {step}: {step_data}")
        if step_data:
            return {key: value for key, value in step_data.items()}
        return {}

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):

        locphoto = form_dict['locphoto']
        plot = form_dict['plot']
        measure = form_dict['measure']
        species = form_dict['species']

        # process image
        image = locphoto['observation_image'].value()
        header, obs_image_encoded = image.split(",", 1)  # Split the header and the base64 data
        obs_image_decoded_data = base64.b64decode(obs_image_encoded)
        timestamp = now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}_user_{self.request.user.id}.png"

        # get or create plot_obj
        plot_obj, created = Plot.objects.get_or_create(
            code=plot['plot'].value(),
            defaults={"source": 'user',
                      "code": plot['plot'].value()}
        )

        observation = Observation()
        observation.user = self.request.user
        observation.image.save(filename, ContentFile(obs_image_decoded_data))
        observation.geo_lat = locphoto['geo_lat'].value()
        observation.geo_lng = locphoto['geo_lng'].value()
        observation.plot = plot_obj
        observation.block = plot['block'].value()
        observation.row = plot['row'].value()
        observation.chlorophyl = measure['chlorophyl'].value() if measure['chlorophyl'].value() != '' else None
        observation.fungal_disease = measure['fungal_disease'].value() if measure['fungal_disease'].value() != '' else None
        observation.eat_marks = measure['eat_marks'].value() if measure['eat_marks'].value() != '' else None
        observation.soil_moisture = measure['soil_moisture'].value() if measure['soil_moisture'].value() != '' else None
        observation.electric_conductivity = measure['electric_conductivity'].value() if measure['electric_conductivity'].value()  != '' else None
        observation.temperature = measure['temperature'].value() if measure['temperature'].value() != '' else None
        observation.save()


        for form in species:
            u_species = form.cleaned_data.get('species')
            coverage = form.cleaned_data.get('coverage')

            if u_species:
                species, created = Species.objects.get_or_create(
                    name=u_species,
                    defaults={"user_generated": True,
                              "name": u_species}
                )

                observation_species = ObservationSpecies()
                observation_species.observation = observation
                observation_species.species = species
                observation_species.coverage = coverage
                observation_species.save()

        return HttpResponseRedirect(reverse_lazy('collector:create_observation_success'))