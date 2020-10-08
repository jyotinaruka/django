from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('books/add', views.add_book),
    path('books/<int:id>', views.book_page),
    path('books/<int:id>/author', views.add_author_in_book),

    path('authors', views.authors),
    path('authors/add', views.add_author),
    path('authors/<int:id>', views.author_page),
    path('authors/<int:id>/book', views.add_book_in_author)


]
