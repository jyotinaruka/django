from django.shortcuts import render, redirect
import random


def index(request):
    if  "game" not in request.session:
        request.session["game"] = random.randint(1, 100)
        request.session["count"] = 0
        request.session["status"] = ""
    return render(request, 'index.html')

def process(request):
    if 'count' not in request.session:
        request.session['count'] = 1
    else:
        request.session['count'] += 1

    guess = request.POST['guess']   # form always gives string
    guess = int(guess)              # covert to int for numbers

    game = request.session['game']
    status = ""
    if request.session['count']>= 5:    # you loose if 5 or more attempts
        status = "loose"
    elif guess < game:                  # your guess is low
        status = "low"
    elif guess > game:                  # your guess is high
        status = "high"
    else:                               # your guess is correct. Winner!
        status = "correct"
    
    request.session['status'] = status
    return redirect("/")
    
def reset(request):
    if "game" in request.session:
        del request.session['game']
    if "count" in request.session:
        del request.session['count']
    if "status" in request.session:
        del request.session['status']
    return redirect('/')

# redirect to leaders.html
def add_winner(request):
    name = request.POST['name']
    attempts = request.session['count']
    
    # create a record
    record = {
        'name': name,
        'attempts': attempts
    }

    # if leaders list does not exist in session then create
    if 'leaders' not in request.session:
        request.session['leaders'] = []

    # get leaders from session
    leaders = request.session['leaders']
    leaders.append(record)

    # update leaders in session
    request.session['leaders'] = leaders
    return redirect('/winnerlist')

def winner_list(request):
    return render(request, 'leaders.html')
