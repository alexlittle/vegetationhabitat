from django import forms
from django.utils.translation import gettext_lazy as _


class ObservationNotesForm(forms.Form):
    notes = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 5, "cols": 40, 'class': 'form-control'}),
        label="Additional Notes (optional)",
        max_length=2000,
        required=False,
        help_text=_("Max 2000 characters.")
    )