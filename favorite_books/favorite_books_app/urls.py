from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('sign_up', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('unique', views.check_unique),
    path('books', views.books),
    path('my_favorite_books', views.my_favorite_books),
    path('add_books', views.add_books),
    path('books/<int:id>', views.book_details),
    path('add_favorite/<int:id>', views.add_favorite),
    path('unfavorite/<int:id>', views.unfavorite),
    path('update_book/<int:id>', views.update_book),
    path('delete_book/<int:id>', views.delete_book)


]
