from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from collector.models import Observation
class HomeView(TemplateView):
    template_name = 'collector/home.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('collector:index')


class MapView(LoginRequiredMixin, TemplateView):
    template_name = 'collector/map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['observations'] = Observation.objects.all()
        return context