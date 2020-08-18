from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9,+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address!"
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use!"
        if len(form['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
        if form['confirm_pw'] != form['password']:
            errors['confirm_pw'] = "Password and Confirmation do not match!"
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    
    def edit(self, form):
        errors = {}
        if len(form['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters!"
        if len(form['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters!"
        if not EMAIL_REGEX.match(form['email']):
            errors['email'] = "Invalid email address!"
        email_check = self.filter(email=form['email'])
        if email_check:
            errors['email'] = "Email already in use!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=16)
    confirm_pw = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()