from django import forms

from .models import Document, Project, Tip


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'start_date']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'doc_type', 'file', 'image', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['title', 'question', 'short_answer', 'category', 'content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }
