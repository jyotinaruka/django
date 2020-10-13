from django.shortcuts import render, redirect
from . models import TvShow
from django.contrib import messages
from django.db import IntegrityError


def index(request):
    return redirect('/shows')


def add_show(request):
    context = {

    }
    return render(request, 'add_show.html', context)


def create_show(request):
    errors = TvShow.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    else:
        title = request.POST['title']
        network = request.POST['network']
        release_date = request.POST['release_date']
        desc = request.POST['desc']
        try:
            tvshow = TvShow.objects.create(title=title, network=network,
                                           release_date=release_date, description=desc)
            return redirect(f"/shows/{tvshow.id}")
        except IntegrityError:
            messages.error(request, "Title must be unique")
            return redirect('/shows/new')


def read_show(request, id):
    tvshow = TvShow.objects.get(id=id)
    context = {
        'show': tvshow
    }
    return render(request, 'display_show.html', context)


def all_shows(request):
    shows_db = TvShow.objects.all()
    context = {
        'shows': shows_db
    }
    return render(request, 'all_shows.html', context)


def edit_show(request, id):
    tvshow = TvShow.objects.get(id=id)
    context = {
        'show': tvshow
    }
    return render(request, 'edit_show.html', context)


def update_show(request, id):
    errors = TvShow.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/shows/{id}/edit")
    else:
        title = request.POST['title']
        network = request.POST['network']
        release_date = request.POST['release_date']
        desc = request.POST['desc']

        tvshow = TvShow.objects.get(id=id)
        tvshow.title = title
        tvshow.network = network
        tvshow.release_date = release_date
        tvshow.description = desc
        try:
            tvshow.save()
            return redirect(f"/shows/{tvshow.id}")
        except IntegrityError:
            messages.error(request, "Title must be unique")
            return redirect(f"/shows/{id}/edit")


def destroy_show(request, id):
    tvshow = TvShow.objects.get(id=id)
    tvshow.delete()
    return redirect('/shows')
