from email.policy import default
from django.conf import settings
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.



class Review(models.Model):
    store_name = models.CharField(max_length=80)                   # 가게이름
    store_address = models.CharField(max_length=100)               # 주소
    image = models.ImageField(upload_to='images/', blank=True)    # 메뉴 사진
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)              # 즐겨찾기
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews') # 즐겨찾기
    phoneNumberRegex = RegexValidator(regex = r"^\+?1?\d{8,15}$")   # 폰번
    phoneNumber = models.CharField(validators = [phoneNumberRegex], max_length = 16, unique = True)
    parking = models.BooleanField(default=False)                   # 주차가능 유무
    price = models.CharField(max_length=15)                         # 가격대
    time = models.TimeField()                                       # 영업시간
    breaktime = models.CharField(max_length=30)                     # 쉬는 시간
    content = models.TextField()                                   # 식당소개


class Comment(models.Model):
    content = models.TextField()                                           # 리뷰 내용
    image = models.ImageField(upload_to='images/', blank=True)             # 이미지
    grade = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)]) # 평점
    created_at = models.DateTimeField(auto_now_add=True)                   # 글 작성일
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comment')
    tag = models.CharField(max_length=32, verbose_name="태그명")            # 소비자 추천
    review = models.ForeignKey(
        Review,
        on_delete = models.CASCADE
    )
