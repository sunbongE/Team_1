from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('update/',views.update,name = 'update'),
    path('<int:user_pk>/',views.profile,name = 'profile'),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path('to_owner/',views.to_owner, name='to_owner'),
    path('check/', views.check, name='check'),
    path('<int:pk>/approve/<int:user_pk>',views.approve,name='approve'),
]

