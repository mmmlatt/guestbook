from django.db import models
from datetime import datetime

# Create your models here.

#Guestbook entry model
class Entry(models.Model):
    entry_text = models.TextField()
    author = models.CharField(max_length=100)
    entry_data = models.DateField(default=datetime.now)
    entry_image = models.ImageField(upload_to="photos", blank=True, default="")