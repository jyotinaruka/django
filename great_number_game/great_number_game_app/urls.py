from django.urls import path
from . import views

urlpatterns = [
    path('',views.index ),
    path('process', views.process),
    path('reset', views.reset),
    path('addwinner', views.add_winner),
    path('winnerlist', views.winner_list)
]
