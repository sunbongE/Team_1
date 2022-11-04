from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Isowner
class CustomUserCreationForm(UserCreationForm):

    class Meta():
        model = get_user_model()
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ('image','first_name','last_name','email',)
    

class IsownerForm(forms.ModelForm):

    class Meta:
        model = Isowner
        fields = (
            "content",
        )
        labels = {
        'content':'사업자 요청',
       
        }