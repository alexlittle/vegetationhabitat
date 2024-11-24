import base64
import collector

from formtools.wizard.views import SessionWizardView

from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.timezone import now

from collector.models import Observation


OLD_FORMS = [("locphoto", collector.forms.ObservationLocationPhotoForm),
         ("plot", collector.forms.ObservationPlotForm),
         ("measure", collector.forms.ObservationMeasurementForm),
         ("species", collector.forms.ObservationSpeciesForm)]

TEMPLATES = {"locphoto": 'collector/wizard/loc_photo.html',
             "plot": 'collector/wizard/plot.html',
             "measure": 'collector/wizard/measurements.html',
             "species": 'collector/wizard/species.html'}

class ObservationWizard(SessionWizardView):
    form_list = [("locphoto", collector.forms.ObservationLocationPhotoForm),
                 ("plot", collector.forms.ObservationPlotForm),
                 ("measure", collector.forms.ObservationMeasurementForm),]

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
            print(f"Going back to step {goto_step}")
            return self.render_goto_step(goto_step)

        return super().post(*args, **kwargs)

    def process_step(self, form):
        """
        Save the current step's form data to storage, even if incomplete.
        """
        step_data = form.data  # Use form.data to ensure even incomplete data is saved
        print(f"Saving data for step {self.steps.current}: {step_data}")
        self.storage.set_step_data(self.steps.current, step_data)
        return super().process_step(form)

    def get_form_initial(self, step):
        """
        Load previously saved data into the form fields when revisiting a step.
        """
        step_data = self.storage.get_step_data(step)
        print(f"Loading data for step {step}: {step_data}")
        if step_data:
            return {key: value for key, value in step_data.items()}
        return {}

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

    def done(self, form_list, form_dict, **kwargs):

        locphoto = form_dict['locphoto']
        image = locphoto['observation_image'].value()
        geo_lat = locphoto['geo_lat'].value()
        geo_lng = locphoto['geo_lng'].value()
        # process image

        header, obs_image_encoded = image.split(",", 1)  # Split the header and the base64 data
        obs_image_decoded_data = base64.b64decode(obs_image_encoded)
        timestamp = now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}_user_{self.request.user.id}.png"

        observation = Observation()
        observation.user = self.request.user
        observation.geo_lat = geo_lat
        observation.geo_lng = geo_lng
        #observation.image.save(filename, ContentFile(obs_image_decoded_data))
        observation.save()

        return HttpResponseRedirect(reverse_lazy('collector:create_observation_success'))