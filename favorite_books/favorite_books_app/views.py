from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from . models import User, Book
import bcrypt


def index(request):
    return render(request, 'login.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        # hash password with bcrypt
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # save user
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name, email=email, password=pw_hash)
        request.session['user_id'] = user.id
        return redirect('/books')


def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/?error=Bad email')
    else:
        email = request.POST['email']
        password = request.POST['password']

        user_list = User.objects.filter(email=email)
        if user_list:
            logged_user = user_list[0]
            if bcrypt.checkpw(password.encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/books')
        else:
            return redirect('/?error=Bad credentials')


def logout(request):
    request.session.clear()
    return redirect('/')


def check_unique(request):
    errors = User.objects.email_validator(request.GET)
    if len(errors) > 0:
        return JsonResponse(errors["email"], safe=False)
    else:
        email = request.GET['email']
        user_list = User.objects.filter(email=email)
        if user_list:
            return JsonResponse("Email already registered.", safe=False)
        else:
            return JsonResponse("true", safe=False)


def books(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    all_books = Book.objects.all()
    context = {
        'user': user,
        'all_books': all_books
    }
    return render(request, 'books.html', context)


def my_favorite_books(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    context = {
        'user': user,
        'my_favorite_books': user.liked_books.all()
    }
    return render(request, 'my_favorite_books.html', context)


def add_books(request):
    if 'user_id' not in request.session:
        return redirect('/')

    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    title = request.POST['title']
    description = request.POST['description']

    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)

    add_book = Book.objects.create(
        title=title, description=description, uploaded_by=user)
    add_book.users_who_like.add(user)
    add_book.save()
    return redirect('/books')


def book_details(request, id):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    book = Book.objects.get(id=id)
    context = {
        "user": user,
        "book": book,
    }
    return render(request, 'book_details.html', context)


def add_favorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    book = Book.objects.get(id=id)
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    book.users_who_like.add(user)
    book.save()
    return redirect(f"/books/{id}")


def unfavorite(request, id):
    if 'user_id' not in request.session:
        return redirect('/')
    book = Book.objects.get(id=id)
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    book.users_who_like.remove(user)
    book.save()
    return redirect(f"/books/{id}")


def update_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    errors = Book.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    title = request.POST['title']
    description = request.POST['description']

    user_id = request.session['user_id']

    book = Book.objects.get(id=id)
    if book.uploaded_by.id == user_id:
        book.title = title
        book.description = description
        book.save()
    return redirect(f"/books/{id}")


def delete_book(request, id):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session['user_id']

    book = Book.objects.get(id=id)
    if book.uploaded_by.id == user_id:
        book.delete()
    return redirect('/books')
