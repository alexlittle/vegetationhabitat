from django import forms
from django.utils.translation import gettext_lazy as _


class ObservationLocationPhotoForm(forms.Form):
    observation_image = forms.CharField(required = True,
                           error_messages={"required": _("Please capture an image")})
    geo_lat = forms.CharField()
    geo_lng = forms.CharField()