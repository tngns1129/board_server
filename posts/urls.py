from django.urls import path

from . import views

urlpatterns = [
    path('', views.posts),
    path('detail/<int:pk>', views.detail),
    path('detail', views.detail),
    path('comments', views.comments),
    path('checkauthor', views.checkAuthor),
]