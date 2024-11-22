from django import forms

class ObservationForm(forms.Form):
    observation_image = forms.CharField(
        label='Observation image',
        widget=forms.TextInput()
    )
    geo_lat = forms.CharField(
        label='Latitude',
        widget=forms.TextInput()
    )
    geo_lng = forms.CharField(
        label='Longitude',
        widget=forms.TextInput()
    )
    plot = forms.CharField(
        label='plot',
        widget=forms.TextInput()
    )