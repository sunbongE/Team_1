from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
     path('', views.index, name='index'),
     path('create/',views.create, name='create'),
     path('<int:detail_pk>/comment/', views.comment_create,name='comment_create'),
    path('<int:detail_pk>/comment/<int:comment_pk>/delete/', views.comment_delete,name='comment_delete'),

]