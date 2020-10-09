from django.shortcuts import render, redirect
from .models import *


def index(request):
    dojo_list = Dojo.objects.all()
    dojo_dict = {}
    for dojo in dojo_list:
        dojo_dict[dojo.id] = {
            "dojo": dojo,
            "ninjas": []
        }

    ninjas = Ninja.objects.all()
    for ninja in ninjas:
        ninja_list = dojo_dict[ninja.dojo.id]["ninjas"]
        ninja_list.append(ninja)
        dojo_dict[ninja.dojo.id]["ninjas"] = ninja_list

    context = {
        'dojo_dict': dojo_dict
    }
    return render(request, 'index.html', context)


def process(request):
    name = request.POST['dojo_name']
    city = request.POST['dojo_city']
    state = request.POST['dojo_state']
    Dojo.objects.create(name=name, city=city, state=state)
    return redirect('/')


def process_ninja(request):
    first_name = request.POST['ninja_first']
    last_name = request.POST['ninja_last']
    dojo_id = request.POST['ninja_dojo']
    Ninja.objects.create(first_name=first_name,
                         last_name=last_name, dojo=Dojo.objects.get(id=dojo_id))
    return redirect('/')


def delete(request, dojo_id):
    # delete ninja of dojo_id
    Ninja.objects.filter(dojo=Dojo.objects.get(id=dojo_id)).delete()
    # delete dojo
    Dojo.objects.get(id=dojo_id).delete()
    return redirect('/')
