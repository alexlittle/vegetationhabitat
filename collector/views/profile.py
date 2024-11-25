import csv
from django.views.generic import View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import HttpResponse

from collector.models import Observation, ObservationSpecies, Species, PlotProperties, Plot


class UserObservationsView(LoginRequiredMixin, ListView):
    template_name = 'collector/user_observations.html'
    paginate_by = 25
    context_object_name = 'observations'

    def get_queryset(self):
        species_prefetch = Prefetch(
            "observationspecies",
            queryset=ObservationSpecies.objects.all(),
        )

        return (
            Observation.objects.filter(user=self.request.user)
            .select_related("plot")
            .prefetch_related("plot__plotproperties_set", species_prefetch)
        )


class UserExportObservationsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="your_model_data.csv"'

        observations = Observation.objects.filter(user=request.user)
        species_list = Species.objects.filter(
            id__in=ObservationSpecies.objects.filter(
                observation__in=observations
            ).values_list('species', flat=True).distinct()).order_by('name')

        plot_properties_list = PlotProperties.objects.values_list('name', flat=True).order_by('name').distinct()

        header_cols = []
        header_cols.extend(['create_date',
                            'image',
                            'geo_lat',
                            'geo_lng',
                            'plot'])

        for p in plot_properties_list:
            header_cols.extend([p])

        header_cols.extend(['block',
                            'row',
                            'chlorophyl',
                            'fungal_disease',
                            'eat_marks',
                            'soil_moisture',
                            'electric_conductivity',
                            'temperature'])

        for s in species_list:
            header_cols.extend([s])


        # Write CSV data
        writer = csv.writer(response)

        writer.writerow(header_cols)

        for o in observations:
            row = []
            row.extend([o.create_date, o.image.url, o.geo_lat, o.geo_lng, o.plot])

            for p in plot_properties_list:
                pp = PlotProperties.objects.filter(plot__observation=o, name=p).first()
                if pp:
                    row.extend([pp.value])
                else:
                    row.extend([''])

            row.extend([o.block,
                                o.row,
                                o.chlorophyl,
                                o.fungal_disease,
                                o.eat_marks,
                                o.soil_moisture,
                                o.electric_conductivity,
                                o.temperature])

            for s in species_list:
                os = ObservationSpecies.objects.filter(observation=o, species=s).first()
                if os:
                    row.extend([os.coverage])
                else:
                    row.extend([''])

            writer.writerow(row)

        return response