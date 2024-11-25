from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch

from collector.models import Observation, ObservationSpecies


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


class UserObservationsView(LoginRequiredMixin, ListView):
    template_name = 'collector/user_observations.html'
    paginate_by = 50
    context_object_name = 'observations'

    def get_queryset(self):
        species_prefetch = Prefetch(
            "observationspecies",  # The related_name in ObservationSpecies
            queryset=ObservationSpecies.objects.all(),  # Optionally filter or annotate
        )

        return (
            Observation.objects.filter(user=self.request.user)
            .select_related("plot")  # Fetch the related Plot object in one query
            .prefetch_related("plot__plotproperties_set", species_prefetch)  # Fetch the related PlotProperties for each Plot
        )
