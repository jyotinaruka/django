from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('process', views.process),
    path('process_ninja', views.process_ninja),
    path('delete/<int:dojo_id>', views.delete)
]
