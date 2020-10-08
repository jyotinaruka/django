from django.shortcuts import render, redirect
from .models import *


def index(request):
    books_db = Book.objects.all()
    context = {
        'books': books_db
    }
    return render(request, 'index.html', context)


def add_book(request):
    title = request.POST['title']
    desc = request.POST['desc']
    Book.objects.create(name=title, desc=desc)
    return redirect('/')


def book_page(request, id):
    book_db = Book.objects.get(id=id)
    authors_db = Author.objects.filter(books__id=id)
    author_id_list = []
    for author in authors_db:
        author_id_list.append(author.id)
    all_authors_db = Author.objects.exclude(id__in=author_id_list)
    context = {
        'book': book_db,
        'authors': authors_db,
        'all_authors': all_authors_db
    }
    return render(request, 'book_page.html', context)


def add_author_in_book(request, id):
    author_id = request.POST['author_id']
    author_db = Author.objects.get(id=author_id)
    book_db = Book.objects.get(id=id)
    author_db.books.add(book_db)
    author_db.save()
    return redirect(f"/books/{book_db.id}")

############### for authors page ############


def authors(request):
    authors_db = Author.objects.all()
    context = {
        'authors': authors_db
    }
    return render(request, 'author.html', context)


def add_author(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    notes = request.POST['notes']
    Author.objects.create(first_name=first_name,
                          last_name=last_name, notes=notes)
    return redirect('/authors')


def author_page(request, id):
    author_db = Author.objects.get(id=id)

    book_id_list = []
    for book in author_db.books.all():
        book_id_list.append(book.id)

    all_books_db = Book.objects.exclude(id__in=book_id_list)
    context = {
        'author': author_db,
        'all_books': all_books_db
    }
    return render(request, 'author_page.html', context)


def add_book_in_author(request, id):
    book_id = request.POST['book_id']
    book_db = Book.objects.get(id=book_id)
    author_db = Author.objects.get(id=id)
    author_db.books.add(book_db)
    author_db.save()
    return redirect(f"/authors/{id}")
