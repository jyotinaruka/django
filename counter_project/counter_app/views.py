from django.shortcuts import render, HttpResponse,redirect


def index(request):
    if 'counter' in request.session:
        request.session['counter'] += 1
    else:
        request.session['counter'] = 1

    if 'visit' in request.session:
        request.session['visit'] += 1
    else:
        request.session['visit'] = 1

    return render(request, 'index.html')


def destroy(request):
    if 'counter' in request.session:
        del request.session['counter']
    return redirect('/')


def increase(request):
    if 'counter' in request.session:
        request.session['counter'] += 1
    else:
        request.session['counter'] = 1

    return redirect('/')

def user(request):
    num = int(request.POST['number'])
    if 'counter' in request.session:
        request.session['counter'] += num-1
    return redirect('/')

    
