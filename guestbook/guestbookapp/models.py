from django.db import models

# Create your models here.

#Guestbook entry model
class Entry(models.Model):
    entry_text = models.TextField()
    author = models.CharField(max_length=100)
    entry_date = models.DateTimeField(auto_now=True)
    entry_image = models.ImageField(upload_to="photos", blank=True, default="")