from django.urls import path

from . import views

urlpatterns = [
    path('', views.posts),
    path('detail', views.detail),
    path('comments', views.comments),
    path('checkauthor', views.checkAuthor),
]