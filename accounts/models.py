from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    
    followings = models.ManyToManyField('self',symmetrical = False, related_name = 'followers')
    is_owner = models.BooleanField(default=False) 
    image = models.ImageField(upload_to='images/', blank=True) # 프로필사진
    @property
    def full_name(self):
        return f'{self.last_name}{self.first_name}'


class Isowner(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)   
    content = models.TextField() 
    