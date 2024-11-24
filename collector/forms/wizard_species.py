from django import forms
from django.forms import formset_factory
from django.utils.translation import gettext_lazy as _



class ObservationSpeciesForm(forms.Form):
    species = forms.CharField(required=False,
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

ObservationSpeciesFormSet = formset_factory(ObservationSpeciesForm,  extra=3, min_num=2)



