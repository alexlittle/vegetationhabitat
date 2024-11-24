from django import forms
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _



class ObservationSpeciesForm(forms.Form):
    species = forms.CharField(required=False,
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': _('Start typing the species name')}))
    coverage = forms.DecimalField(max_digits=4,
                                  decimal_places=2,
                                  required=False,
                                  initial=None,
                                  min_value=0,
                                  max_value=100,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()  # Make sure to call the parent class's clean method
        species = cleaned_data.get('species')
        coverage = cleaned_data.get('coverage')

        # Check if either species or coverage is missing and raise the appropriate error
        if species and not coverage:  # species is provided but coverage is not
            raise ValidationError(_("If a species is entered, you must enter the coverage."))
        elif not species and coverage:  # coverage is provided but species is not
            raise ValidationError(_("If coverage is entered, you must enter the species."))

        return cleaned_data

class BaseObservationSpeciesFormSet(BaseFormSet):
     def clean(self):
         """Checks that no two articles have the same title."""
         if any(self.errors):
             # Don't bother validating the formset unless each form is valid on its own
             return
         species_set = set()
         for form in self.forms:
             if self.can_delete and self._should_delete_form(form):
                 continue
             species = form.cleaned_data.get("species")
             if species: # only add if not nothing
                 if species in species_set:
                     raise ValidationError("Cannot enter the same species twice")
                 species_set.add(species)

         if len(species_set) < 1:
             raise ValidationError("Please enter at least one species")

ObservationSpeciesFormSet = formset_factory(ObservationSpeciesForm,  extra=3, min_num=2, formset=BaseObservationSpeciesFormSet)



