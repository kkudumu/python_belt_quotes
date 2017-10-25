from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Quote(models.Model):
    quote_author = models.CharField(max_length=255, null = True)
    content = models.TextField(max_length=5000, null = True)
    quote_submit = models.ForeignKey(User, related_name= "quote_submit", null = True)
    favorite = models.ManyToManyField(User, related_name="favorite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)