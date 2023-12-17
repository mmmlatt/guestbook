from django.db import models

# Create your models here.

#Guestbook entry model
class Entry(models.Model):
    entry_text = models.TextField()
    author = models.CharField(max_length=100)