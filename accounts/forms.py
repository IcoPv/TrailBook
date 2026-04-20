from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Profile

UserModel = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserModel
        fields = ["username", "email", "first_name", "last_name"]


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserModel.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email


class ProfileForm(forms.ModelForm):

    username = forms.CharField(disabled=True, required=False)

    class Meta:
        model = Profile
        fields = ["bio", "avatar", "vehicle_type", "riding_experience", "location"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['username'].initial = self.instance.user.username
