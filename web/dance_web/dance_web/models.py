from django.db import models
import datetime
from . import EVENT_CHOICES

class Event(models.Model):
    title = models.CharField()
    slug = models.SlugField()
    link = models.CharField()
    start = models.DateTimeField("DateTime", default=datetime.datetime.now)
    end = models.DateTimeField("DateTime", default=datetime.datetime.now)
    town = models.CharField()
    adress = models.CharField()
    lector = models.CharField()
    contact = models.CharField()
    description = models.TextField()
    image = models.ImageField()
    price = models.CharField()
    locationId = models.DecimalField()
    type = models.CharField(choices=EVENT_CHOICES)

def __str__(self):
    return self.title