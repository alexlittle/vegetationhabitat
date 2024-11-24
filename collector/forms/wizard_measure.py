from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ObservationMeasurementForm(forms.Form):
    chlorophyl = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'step': '1', 'class': 'form-control'}),
        help_text=_("Enter the chlorophyl value as a whole number (0-9999, no decimals).")
    )
    fungal_disease = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        help_text = _("Enter the fungal disease level with up to two decimal places.")
    )
    eat_marks = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'step': '0.01', 'class': 'form-control'}),
        help_text = _("Enter the eat marks level with up to two decimal places.")
    )
    soil_moisture = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        help_text=_("Enter the soil moisture level with up to one decimal place.")
    )
    electric_conductivity = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=0,
        widget=forms.NumberInput(attrs={'step': '1', 'class': 'form-control'}),
        help_text=_("Enter the electric conductivity value as a whole number (0-9999, no decimals).")
    )
    temperature = forms.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'step': '0.1', 'class': 'form-control'}),
        help_text=_("Enter the temperature level with up to one decimal place.")
    )

