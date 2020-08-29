from django.db import models
import re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2 or len(postData['last_name']) < 2:
            errors['name'] = "First name and last name must be at least 2 characters"
        if len(postData['email']) == 0:
            errors['email_e'] = "Email field cannot be empty"
        email_checker = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_checker.match(postData['email']):
            errors['email'] = "Email must be valid"
        if len(postData['pw']) < 8:
            errors['pw'] = "Password must be at least 8 characters"
        if postData['pw'] != postData['conf_pw']:
            errors['conf_pw'] = "Password and Confirm password must match"
        return errors

class BookManager(models.Manager):
    def validate_book(self, postData):
        errors = {}
        if len(postData['title']) == 0:
            errors['title'] = "Title is required!"
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters"
        return errors

        


class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="uploaded_books", on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
