from django import forms

from gallery.models import Photo
from waypoints.models import Waypoint


class PhotoUploadForm(forms.ModelForm):

    MAX_UPLOAD_SIZE = 5 * 1024 * 1024
    ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp']

    class Meta:
        model = Photo
        fields = ['image', 'caption', 'waypoint']

    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super().__init__(*args, **kwargs)
        if self.trip:
            self.fields['waypoint'].queryset = self.trip.waypoints.all()
            self.fields['waypoint'].required = False
            self.fields['waypoint'].empty_label = 'Not linked to a waypoint'

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError('Image must be smaller than 5MB.')
            if hasattr(image, 'content_type') and image.content_type not in self.ALLOWED_CONTENT_TYPES:
                raise forms.ValidationError('Only JPEG, PNG, and WebP images are allowed.')
        return image