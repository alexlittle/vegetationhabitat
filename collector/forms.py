from django import forms

class ObservationForm(forms.Form):
    observation_image = forms.CharField(required = True,
                           error_messages={"required": "Please capture an image"})
    geo_lat = forms.CharField()
    geo_lng = forms.CharField()
    plot = forms.CharField(required = True,
                           error_messages={"required": "Please enter a plot"})

