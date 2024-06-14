from django.db import models
import datetime

class EventType(models.IntegerChoices):
        EVENT = 1, 'Večerní akce'
        WORKSHOP = 2, 'Workshop'
        SPECIAL = 3, 'Speciální akce' 

class Location(models.Model):
    name = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    adress = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    link = models.CharField(max_length=256, null=True, blank=True)
    start = models.DateTimeField("DateTime", default=datetime.datetime.now)
    end = models.DateTimeField("DateTime", default=datetime.datetime.now)
    lector = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(null=True, blank=True)
    price = models.CharField(max_length=50, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    type = models.IntegerField(choices=EventType.choices, default=None)

    def __str__(self):
        return self.title
    
    def beginning(self):
        return self.link[:50] + "..."
    
class Lector(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    description = models.TextField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return self.firstName

class EventLector(models.Model):
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    lectorId = models.ForeignKey(Lector, on_delete=models.CASCADE)
    class Meta:
     constraints = [
          models.UniqueConstraint(fields=['eventId', 'lectorId'], name='un_eventlector')
     ]
