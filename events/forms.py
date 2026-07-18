from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Event
        fields = ['title', 'date', 'event_type', 'description', 'location']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
