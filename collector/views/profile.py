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
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="your_model_data.csv"'

        # Fetch observations for the user
        observations = (
            Observation.objects.filter(user=request.user)
            .select_related("plot")  # Load the related Plot in a single query
            .prefetch_related(
                Prefetch(
                    "plot__plotproperties_set",  # Adjust to follow Plot to PlotProperties relationship
                    queryset=PlotProperties.objects.order_by("name"),
                    to_attr="prefetched_plot_properties",  # Store prefetched properties in a custom attribute
                )
            )
        )

        # Fetch species related to observations
        species_ids = (
            ObservationSpecies.objects.filter(observation__in=observations)
            .values_list("species", flat=True)
            .distinct()
        )
        species_list = list(Species.objects.filter(id__in=species_ids).order_by("name"))

        # Fetch distinct plot properties
        plot_properties_list = list(
            PlotProperties.objects.values_list("name", flat=True)
            .distinct()
            .order_by("name")
        )

        # Define header columns
        header_cols = [
            "create_date",
            "image",
            "geo_lat",
            "geo_lng",
            "plot",
            *plot_properties_list,
            "block",
            "row",
            "chlorophyl",
            "fungal_disease",
            "eat_marks",
            "soil_moisture",
            "electric_conductivity",
            "temperature",
            *species_list,
        ]

        # Write CSV data
        writer = csv.writer(response)
        writer.writerow(header_cols)

        for o in observations:
            # Base observation data
            row = [
                o.create_date,
                o.image.url if o.image else "",
                o.geo_lat,
                o.geo_lng,
                o.plot,
            ]

            # Add plot properties
            plot_properties = (
                {pp.name: pp.value for pp in o.plot.prefetched_plot_properties}
                if o.plot and hasattr(o.plot, "prefetched_plot_properties")
                else {}
            )
            row.extend(plot_properties.get(p, "") for p in plot_properties_list)

            # Add other observation fields
            row.extend(
                [
                    o.block,
                    o.row,
                    o.chlorophyl,
                    o.fungal_disease,
                    o.eat_marks,
                    o.soil_moisture,
                    o.electric_conductivity,
                    o.temperature,
                ]
            )

            # Add species coverage
            species_coverage = {
                os.species.id: os.coverage
                for os in ObservationSpecies.objects.filter(observation=o)
            }
            row.extend(species_coverage.get(s.id, "") for s in species_list)

            writer.writerow(row)

        return response
