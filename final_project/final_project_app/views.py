from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from . models import User, Message, Comment
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
        return redirect('/wall')


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
                return redirect('/wall')
        else:
            return redirect('/?error=Bad credentials')


def logout(request):
    del request.session['user_id']
    return redirect('/')


def wall(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        posts = Message.objects.all()
        context = {
            'user': user,
            'posts': posts
        }
        return render(request, 'wall.html', context)


def post_msg(request):
    if 'user_id' not in request.session:
        return redirect('/')

    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wall')
    else:
        msg = request.POST['message']
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        Message.objects.create(message=msg, user=user)
        return redirect('/wall')


def post_comment(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        comment = request.POST['comment']
        post_id = request.POST['post_id']
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        message = Message.objects.get(id=post_id)
        Comment.objects.create(comment=comment, user=user, message=message)
        return redirect('/wall')


def delete_message(request, id):
    message = Message.objects.get(id=id)
    message.delete()
    return redirect('/wall')
