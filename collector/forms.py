from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _

class ObservationLocationPhotoForm(forms.Form):
    observation_image = forms.CharField(required = True,
                           error_messages={"required": _("Please capture an image")})
    geo_lat = forms.CharField()
    geo_lng = forms.CharField()


class ObservationPlotForm(forms.Form):
    YES_NO_CHOICES = [
        ('1', _('Yes')),
        ('0', _('No')),
    ]
    plot = forms.CharField(required = True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}),
                           error_messages={"required": _("Please enter a plot")})
    block = forms.CharField(required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            error_messages={"required": _("Please enter a block")})
    row = forms.CharField(required=True,
                          widget=forms.TextInput(attrs={'class': 'form-control'}),
                          error_messages={"required": _("Please enter a row")})
    '''
    fertilization = forms.ChoiceField(required=True,
                                      choices=YES_NO_CHOICES,
                                      widget=forms.RadioSelect,
                          error_messages={"required": _("Please enter fertilization")})
    cutting = forms.ChoiceField(required=True,
                                        choices=YES_NO_CHOICES,
                                    widget=forms.RadioSelect,
                          error_messages={"required": _("Please enter cutting")})
    '''


class ObservationMeasurementForm(forms.Form):
    chlorophyl = forms.DecimalField(
        max_digits=4,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'step': '1', 'class': 'form-control'})
    )
    fungal_disease = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'})
    )
    eat_marks = forms.DecimalField(
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'})
    )
    soil_moisture = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'})
    )
    electric_conductivity = forms.DecimalField(
        max_digits=4,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'step': '1', 'class': 'form-control'})
    )
    temperature = forms.DecimalField(
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'})
    )

class ObservationSpeciesForm(forms.Form):
    species = forms.CharField(required = True,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': _('Start typing the species name')}),
                           error_messages={"required": _("Please enter a species")})
    coverage = forms.DecimalField(max_digits=4,
                                  decimal_places=2,
                                  required=False,
                                  initial=None,
                                  min_value=0,
                                  max_value=100,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}),)

ObservationSpeciesFormSet = formset_factory(ObservationSpeciesForm,  extra=3, min_num=1)


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': ''}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': ''
        }
))
