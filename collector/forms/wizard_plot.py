from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class ObservationPlotForm(forms.Form):

    plot = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    block = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    row = forms.CharField(required=False,
                          widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean_plot(self):
        if self.cleaned_data.get('plot') == "":
            raise ValidationError(_("Please enter a plot"))

    def clean_block(self):
        if self.cleaned_data.get('block') == "":
            raise ValidationError(_("Please enter a block"))

    def clean_row(self):
        if self.cleaned_data.get('row') == "":
            raise ValidationError(_("Please enter a row"))