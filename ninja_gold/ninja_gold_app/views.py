from django.shortcuts import render,redirect
import random
from time import strftime
import datetime

key_activities = 'activities'

def index(request):
    if 'gold' not in request.session:
        request.session['gold'] = 0
    if key_activities not in request.session:
        request.session[key_activities] = []
    print('gold', request.session['gold'])
    print(key_activities, request.session[key_activities])
    return render(request, 'index.html')

def process(request):
    action = request.POST['action']
    now = datetime.datetime.now()
    if action == "farm":
        earn = random.randint(10, 20)
        activity = {
            'type': action,
            'money': earn,
            'date': now.strftime("%Y/%m/%d %H:%M %p")
        }
        request.session['gold'] = request.session['gold'] + earn
        activities = request.session[key_activities]
        activities.append(activity)
        request.session[key_activities] = activities
    elif action == "cave":
        earn = random.randint(5, 10)
        activity = {
            'type': action,
            'money': earn,
            'date': now.strftime("%Y/%m/%d %H:%M %p")
        }
        request.session['gold'] = request.session['gold'] + earn
        activities = request.session[key_activities]
        activities.append(activity)
        request.session[key_activities] = activities
    elif action == "house":
        earn = random.randint(2, 5)
        activity = {
            'type': action,
            'money': earn,
            'date': now.strftime("%Y/%m/%d %H:%M %p")
        }
        request.session['gold'] = request.session['gold'] + earn
        activities = request.session[key_activities]
        activities.append(activity)
        request.session[key_activities] = activities
    elif action == "casino":
        earn = random.randint(-50, 50)
        activity = {
            'type': action,
            'money': earn,
            'date': now.strftime("%Y/%m/%d %H:%M %p")
        }
        request.session['gold'] = request.session['gold'] + earn
        activities = request.session[key_activities]
        activities.append(activity)
        request.session[key_activities] = activities
    return redirect('/')

def reset(request):
    if 'gold' in request.session:
        del request.session['gold']
    if key_activities in request.session:
        del request.session[key_activities]
    return redirect('/')

