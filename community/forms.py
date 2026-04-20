from django import forms

from community.models import TrailNote


class TrailNoteForm(forms.ModelForm):

    class Meta:
        model = TrailNote
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Share your thoughts, tips, or warnings about this trip...',
            }),
        }

    def clean_body(self):
        body = self.cleaned_data.get('body', '').strip()
        if len(body) < 10:
            raise forms.ValidationError('Trail notes must be at least 10 characters long.')
        return body