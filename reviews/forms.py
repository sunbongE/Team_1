from django import forms
from .models import Review, Comment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields=(
            'store_name',
            'store_address',
            'image',
            'phoneNumber',
            'parking',
            'time',
            'price',
            'breaktime',
            'content',
        )

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = (
            "content",
            'image',
            'grade',
            'tag',
        )
        labels = {
        'content':'맛 평가',
        'image':'음식 사진',
        'grade': '평점',
        }