from django import forms

from .models import Article, ArticleImage, Event


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


class ArticleForm(forms.ModelForm):
    published_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Article
        fields = ['title', 'summary', 'body', 'image', 'published_at']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 2}),
            'body': forms.Textarea(attrs={'rows': 10}),
        }


class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ['image', 'caption']
