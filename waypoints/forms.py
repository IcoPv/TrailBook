from django import forms
from django.forms.models import inlineformset_factory

from trips.models import Trip
from waypoints.models import Waypoint


class WaypointForm(forms.ModelForm):

    class Meta:
        model = Waypoint
        fields = [
            'name', 'description', 'latitude', 'longitude', 'elevation',
            'categories', 'order', 'arrival_date',
        ]
        widgets = {
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'categories': forms.CheckboxSelectMultiple(),
            'description': forms.Textarea(attrs={'rows': 3}),
        }



class WaypointFormsetForm(forms.ModelForm):

    class Meta:
        model = Waypoint
        fields = [
            'name', 'latitude', 'longitude', 'categories', 'order',
        ]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
        }


WaypointFormset = inlineformset_factory(
    Trip,
    Waypoint,
    form = WaypointFormsetForm,
    extra = 3,
    can_delete = True,
)

