from django import forms

from trips.choices import Difficulty, VehicleTypeTrips
from trips.models import Trip


class TripForm(forms.ModelForm):

    class Meta:
        model = Trip
        fields = ['title', 'description', 'difficulty', 'vehicle_type', 'tags', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.CheckboxSelectMultiple(),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError({
                'end_date': 'End date cannot be before start date!'
            })

        return cleaned_data



class TripSearchForm(forms.Form):

    query = forms.CharField(
        required = False,
        widget = forms.TextInput(attrs={'placeholder': 'Search trips...'}),
    )

    difficulty = forms.ChoiceField(
        required = False,
        choices = [('', 'All Difficulties')] + Difficulty.choices,
    )

    vehicle_type = forms.ChoiceField(
        required = False,
        choices = [('', 'All Vehicles')] + VehicleTypeTrips.choices,
    )