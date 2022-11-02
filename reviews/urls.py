from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
     path("", views.main, name="main"),
     path('reviews/', views.index, name='index'),
     path('create/',views.create, name='create'),
     path('<int:detail_pk>/comment/', views.comment_create,name='comment_create'),
     path('<int:detail_pk>/comment/<int:comment_pk>/delete/', views.comment_delete,name='comment_delete'),
     path('<int:detail_pk>/', views.detail, name='detail'),
     path('<int:detail_pk>/update/', views.update, name='update'),
     path('<int:detail_pk>/delete/', views.delete, name='delete'),
     path('search/', views.search, name='search')
]