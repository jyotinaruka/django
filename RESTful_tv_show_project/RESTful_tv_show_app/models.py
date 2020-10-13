from django.db import models
from datetime import datetime


class TvShowManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        if len(data["title"]) < 2:
            errors["title"] = "Tv Show title should have at least 2 characters."
        if len(data["network"]) < 3:
            errors["network"] = "Tv Show network should have at least 3 characters."

        if len(data["release_date"]) == 0:
            errors["release_date"] = "Tv Show release date is required."
        if len(data["release_date"]) > 0 and datetime.strptime(data["release_date"], "%Y-%m-%d") >= datetime.now():
            errors["release_date"] = "Tv Show release date should be in the past."

        if len(data["desc"]) > 0 and len(data["desc"]) < 10:
            errors["desc"] = "Tv Show description should have at least 10 characters."
        return errors


class TvShow(models.Model):
    title = models.CharField(max_length=255, unique=True)
    network = models.CharField(max_length=255)
    release_date = models.DateField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TvShowManager()
