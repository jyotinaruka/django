from django.db import models
from datetime import datetime
import re


class UserManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        if len(data["first_name"]) < 2:
            errors["first_name"] = "First name should be atleast 2 character."
        if len(data["last_name"]) < 2:
            errors["last_name"] = "Last name should be atleast 2 character."

        if len(data["password"]) < 8:
            errors["password"] = "Password should be atleast 8 characters."
        if (data["confirm_pw"] != data["password"]):
            errors["confirm_pw"] = "Password and Confirm PW do not match."

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Please enter a valid email."
        return errors

    def login_validator(self, data):
        errors = {}
        if len(data["email"]) == 0:
            errors['email'] = "Email should not be empty"
        if len(data["password"]) == 0:
            errors["password"] = "Password should not be empty"
        return errors

    def email_validator(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']):
            errors['email'] = "Please enter a valid email."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class MessageManager(models.Manager):
    def basic_validator(self, data):
        errors = {}
        if len(data["message"]) < 2:
            errors["message"] = "Message should be atleast 2 character."
        return errors


class Message(models.Model):
    user = models.ForeignKey(
        User, related_name="messages", on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()


class Comment(models.Model):
    user = models.ForeignKey(
        User, related_name="users", on_delete=models.CASCADE)
    message = models.ForeignKey(
        Message, related_name="comments", on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
