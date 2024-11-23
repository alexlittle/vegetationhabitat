import base64

from django.core.files.base import ContentFile
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.timezone import now

from .forms import ObservationForm
from .models import Observation
from django import forms

class HomeView(TemplateView):
    template_name = 'collector/home.html'

class RecordObservationView(LoginRequiredMixin, FormView):
    template_name = 'collector/observation.html'
    form_class = ObservationForm
    success_url = reverse_lazy('collector:create_observation_success')

    def form_valid(self, form):
        if not form.is_valid():
            # Handle form validation errors here
            return self.form_invalid(form)

        # Handle valid form submission here
        observation_image = form.cleaned_data['observation_image']
        geo_lat = form.cleaned_data['geo_lat']
        geo_lng = form.cleaned_data['geo_lng']
        plot = form.cleaned_data['plot']

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
        observation.plot = plot
        observation.image.save(filename, ContentFile(obs_image_decoded_data))
        observation.save()

        # Return the response to indicate success
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class ObservationSuccessView(TemplateView):
    template_name = 'collector/observation_success.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('collector:index')

class MapView(LoginRequiredMixin, TemplateView):
    template_name = 'collector/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['observations'] = Observation.objects.all()
        return context
