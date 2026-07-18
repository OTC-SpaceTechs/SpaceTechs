from django import forms

from .models import PurchaseRequest


class PurchaseRequestCreateForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['project', 'amount', 'purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 4}),
        }


class PurchaseRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = PurchaseRequest
        fields = ['project', 'amount', 'purpose', 'status']
        widgets = {
            'purpose': forms.Textarea(attrs={'rows': 4}),
        }
