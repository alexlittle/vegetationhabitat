from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class ObservationForm(forms.Form):
    observation_image = forms.CharField(required = True,
                           error_messages={"required": "Please capture an image"})
    geo_lat = forms.CharField()
    geo_lng = forms.CharField()
    plot = forms.CharField(required = True,
                           error_messages={"required": "Please enter a plot"})



class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'hello'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'hi',
        }
))
