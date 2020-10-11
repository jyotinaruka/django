from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('sign_up', views.register),
    path('login', views.login),
    path('wall', views.wall),
    path('logout', views.logout),
    path('post_msg', views.post_msg),
    path('post_comment', views.post_comment),
    path('delete_message/<int:id>', views.delete_message)
]
