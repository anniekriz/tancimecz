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

class Event(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    link = models.CharField(max_length=256)
    start = models.DateTimeField("DateTime", default=datetime.datetime.now)
    end = models.DateTimeField("DateTime", default=datetime.datetime.now)
    lector = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField()
    price = models.CharField(max_length=50)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)
    type = EventType.choices

    def __str__(self):
        return self.title
    
class Lector(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    image = models.ImageField()
    description = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    link = models.CharField(max_length=256)

class EventLector(models.Model):
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    lectorId = models.ForeignKey(Lector, on_delete=models.CASCADE)
    class Meta:
     constraints = [
          models.UniqueConstraint(fields=['eventId', 'lectorId'], name='un_eventlector')
     ]
