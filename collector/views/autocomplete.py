from django.http import JsonResponse
from django.db.models import Prefetch
from django.views import View

from collector.models import Species, Plot, PlotProperties

class SpeciesAutocompleteView(View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')

        if len(query) < 3:
            return JsonResponse([], safe=False)

        species = Species.objects.filter(name__istartswith=query, user_generated=False).order_by('name')[:25]
        suggestions = [species.name for species in species]

        return JsonResponse(suggestions, safe=False)

class PlotAutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')

        if len(query) < 2:
            return JsonResponse([], safe=False)

        plots = (
            Plot.objects.filter(code__istartswith=query)
            .prefetch_related(
                Prefetch(
                    'plotproperties_set',
                    queryset=PlotProperties.objects.only('name', 'value'),
                    to_attr='prefetched_properties'
                )
            )
            .order_by('code')[:25]
        )

        suggestions = [
            {
                'code': plot.code,
                'properties': [
                    {'name': prop.name, 'value': prop.value}
                    for prop in plot.prefetched_properties
                ]
            }
            for plot in plots
        ]

        return JsonResponse(suggestions, safe=False)