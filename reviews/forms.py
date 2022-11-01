from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields=[
            'store_name',
            'store_address',
            'image',
            'phoneNumber',
            'parking',
            'time',
            'breaktime',
            'content',
            'tag',
        ]