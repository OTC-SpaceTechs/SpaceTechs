from django import forms

from .models import Member, OfficerHistory


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['user', 'active_status', 'major', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class OfficerHistoryForm(forms.ModelForm):
    class Meta:
        model = OfficerHistory
        fields = ['role', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
