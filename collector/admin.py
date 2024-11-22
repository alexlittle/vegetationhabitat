from django.contrib import admin
from django.utils.html import format_html
from collector.models import Observation


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'user', 'create_date', 'geo_lat', 'geo_lng', 'plot')
    readonly_fields = ('image_thumb',)

    def image_thumb(self, obj):
        if obj.image:  # Check if the image exists
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "No Image"
