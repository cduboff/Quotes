from django.db import models
from datetime import datetime
from log_red.models import User
# Create your models here.

class QuoteManager(models.Manager):
    def validator(self, form):
        errors = {}
        if len(form['content']) < 10:
            errors['content'] = "Content of Quote must be at least 10 characters!"
        if len(form['author']) < 3:
            errors['author'] = "Author name must be at least 3 characters!"
        return errors
        
class Quote(models.Model):
    content = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name="likes")
    poster = models.ForeignKey(User, related_name="quotes", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()
