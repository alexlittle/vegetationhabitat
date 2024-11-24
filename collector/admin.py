from django.contrib import admin
from django.utils.html import format_html
from collector.models import Observation, Species, ObservationSpecies


class ObservationSpeciesInline(admin.TabularInline):
    model = ObservationSpecies
    readonly_fields = ('observation', 'species',)

@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'user', 'create_date', 'geo_lat', 'geo_lng', 'plot')
    readonly_fields = ('image_thumb',)

    inlines = [
        ObservationSpeciesInline,
    ]

    def image_thumb(self, obj):
        if obj.image:  # Check if the image exists
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"

@admin.register(Species)
class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_generated')
    search_fields = ('name',)

@admin.register(ObservationSpecies)
class ObservationSpeciesAdmin(admin.ModelAdmin):
    list_display = ('observation', 'species', 'coverage')
    readonly_fields = ('observation', 'species',)