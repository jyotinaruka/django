from django.shortcuts import render, HttpResponse
from time import strftime
import datetime

def index(request):
    now = datetime.datetime.now()
    context = {
        "date": now.strftime("%b %d, %Y"),
        "time": now.strftime(" %H:%M %p")

    }
    return render(request, 'index.html', context)

