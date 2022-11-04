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
            'endtime',
            'price',
            'breaktime',
            'content',
        )
        labels={
            'store_name':'상호명',
            'store_address':'주소',
            'image':'사진',
            'phoneNumber':'가게 번호',
            'parking':'주차',
            'time':'영업 시간',
            'price':'가격대',
            'breaktime':'휴식 시간',
            'content':'가게 소개',
        }

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