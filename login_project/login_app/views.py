from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from . models import User
import bcrypt


def index(request):
    return render(request, 'login.html')


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        user_id = request.session['user_id']
        user = User.objects.get(id=user_id)
        context = {
            'user': user
        }
        return render(request, 'success.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        birthday = request.POST['birthday']
        email = request.POST['email']
        password = request.POST['password']
        # hash password with bcrypt
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # save user
        user = User.objects.create(first_name=first_name,
                                   last_name=last_name, birthday=birthday, email=email, password=pw_hash)
        request.session['user_id'] = user.id
        return redirect('/success')


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
                return redirect('/success')
        else:
            return redirect('/?error=Bad credentials')


def logout(request):
    del request.session['user_id']
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
