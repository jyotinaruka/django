from django.urls import path
from . import views

urlpatterns = [

    path('', views.index),
    path('shows/new', views.add_show),
    path('shows/create', views.create_show),
    path('shows/<int:id>', views.read_show),
    path('shows', views.all_shows),
    path('shows/<int:id>/edit', views.edit_show),
    path('shows/<int:id>/update', views.update_show),
    path('shows/<int:id>/destroy', views.destroy_show),
]
