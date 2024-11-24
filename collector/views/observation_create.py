import base64

from django.core.files.base import ContentFile
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils.timezone import now

from collector.forms import ObservationLocationPhotoForm, ObservationPlotForm, ObservationMeasurementForm, ObservationSpeciesFormSet
from collector.models import Observation, Species, ObservationSpecies


class ObservationLocationPhotoView(LoginRequiredMixin, FormView):
    template_name = 'collector/observation_loc_photo.html'
    form_class = ObservationLocationPhotoForm
    success_url = reverse_lazy('collector:create_observation_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step_number'] = 1
        context['step_count'] = 4
        return context

    def form_valid(self, form):

        # Handle valid form submission here
        observation_image = form.cleaned_data['observation_image']
        geo_lat = form.cleaned_data['geo_lat']
        geo_lng = form.cleaned_data['geo_lng']

        # process image
        header, obs_image_encoded = observation_image.split(",", 1)  # Split the header and the base64 data
        obs_image_decoded_data = base64.b64decode(obs_image_encoded)
        timestamp = now().strftime('%Y%m%d_%H%M%S')  # Format: YYYYMMDD_HHMMSS
        filename = f"{timestamp}_user_{self.request.user.id}.png"

        # Process data as needed (e.g., save to database, send email, etc.)
        observation = Observation()
        observation.user = self.request.user
        observation.geo_lat = geo_lat
        observation.geo_lng = geo_lng
        observation.image.save(filename, ContentFile(obs_image_decoded_data))
        observation.save()

        self.success_url = reverse('collector:create_observation_plot', kwargs={'id': observation.id})
        # Return the response to indicate success
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ObservationPlotView(LoginRequiredMixin, FormView):
    template_name = 'collector/observation_plot.html'
    form_class = ObservationPlotForm
    success_url = reverse_lazy('collector:create_observation_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step_number'] = 2
        context['step_count'] = 4
        return context

    def form_valid(self, form):

        observation_id = self.kwargs.get('id')
        # Fetch the existing observation
        try:
            observation = Observation.objects.get(id=observation_id, user=self.request.user)
        except Observation.DoesNotExist:
            form.add_error(None, "Observation not found or you don't have permission to modify it.")
            return self.form_invalid(form)

        # Handle valid form submission here
        observation.plot = form.cleaned_data['plot']
        observation.block = form.cleaned_data['block']
        observation.row = form.cleaned_data['row']
        observation.save()

        self.success_url = reverse('collector:create_observation_measurements', kwargs={'id': observation.id})
        # Return the response to indicate success
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ObservationMeasurementsView(LoginRequiredMixin, FormView):
    template_name = 'collector/observation_measurements.html'
    form_class = ObservationMeasurementForm
    success_url = reverse_lazy('collector:create_observation_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step_number'] = 3
        context['step_count'] = 4
        return context

    def form_valid(self, form):

        observation_id = self.kwargs.get('id')
        try:
            observation = Observation.objects.get(id=observation_id, user=self.request.user)
        except Observation.DoesNotExist:
            form.add_error(None, "Observation not found or you don't have permission to modify it.")
            return self.form_invalid(form)

        observation.chlorophyl = form.cleaned_data['chlorophyl']
        observation.fungal_disease = form.cleaned_data['fungal_disease']
        observation.eat_marks = form.cleaned_data['eat_marks']
        observation.soil_moisture = form.cleaned_data['soil_moisture']
        observation.electric_conductivity = form.cleaned_data['electric_conductivity']
        observation.temperature = form.cleaned_data['temperature']
        observation.save()

        self.success_url = reverse('collector:create_observation_species', kwargs={'id': observation.id})
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class ObservationSpeciesView(LoginRequiredMixin, FormView):
    template_name = 'collector/observation_species.html'
    form_class = ObservationSpeciesFormSet
    success_url = reverse_lazy('collector:create_observation_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['step_number'] = 4
        context['step_count'] = 4
        context['formset'] = ObservationSpeciesFormSet()
        return context

    def form_valid(self, formset):

        observation_id = self.kwargs.get('id')
        # Fetch the existing observation
        try:
            observation = Observation.objects.get(id=observation_id, user=self.request.user)
        except Observation.DoesNotExist:
            formset.add_error(None, "Observation not found or you don't have permission to modify it.")
            return self.form_invalid(formset)

        for form in formset:
            if form.is_valid():
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

        # Return the response to indicate success
        return super().form_valid(formset)

    def form_invalid(self, formset):
        return self.render_to_response(self.get_context_data(formset=formset))


class ObservationSuccessView(TemplateView):
    template_name = 'collector/wizard/success.html'






