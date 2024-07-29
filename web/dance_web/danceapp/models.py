from django.db import models
import datetime
from django.contrib.auth.models import User

class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/')
    description = models.TextField()
    phone = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        ordering = ['firstName'] #řazení lektorů podle abecedy

    def __str__(self):
        return f"{self.firstName} {self.lastName or ''}".strip()
    
class Location(models.Model):
    coordinates = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    lector = models.ForeignKey(Lector, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.town}, {self.address}"

class EventGroup(models.Model):
    lector = models.ManyToManyField(Lector, verbose_name="Lektor")
    location = models.ForeignKey(Location, verbose_name="Místo konání", on_delete=models.PROTECT)
    startTime = models.TimeField(verbose_name="Začátek", default='18:00')
    endTime = models.TimeField(verbose_name="Konec (nepovinné)", default='19:00', null=True, blank=True)
    description = models.TextField(verbose_name="Popis")
    image = models.ImageField(verbose_name="Obrázek", upload_to='images/')

    def __str__(self):
        startTime = self.startTime.strftime('%H:%M')
        endTime = self.endTime.strftime('%H:%M')
        if self.endTime:
            return f"{self.location.town} {startTime}-{endTime}"
        return f"{self.location.town} {startTime}"

class Event(models.Model):
    parent = models.ForeignKey(EventGroup, verbose_name="Event Group", on_delete=models.PROTECT)
    date = models.DateField(verbose_name="Datum", default=datetime.date.today)
    description = models.TextField(verbose_name="Dodatečný popis", null=True, blank=True)

    def __str__(self):
        startTime = self.parent.startTime.strftime('%H:%M')
        endTime = self.endTime.strftime('%H:%M')
        date = self.date.strftime('%d.%m. %Y')
        if self.parent.endTime:
            return f"{self.parent.location.town} {date} {startTime}-{endTime}"
        return f"{self.parent.location.town} {date} {startTime}"

class Workshop(models.Model):
    title = models.CharField(verbose_name="Název", max_length=101)
    link = models.CharField(verbose_name="Odkaz (nepovinné)", max_length=256, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name="Místo konání", on_delete=models.PROTECT)
    start = models.DateField(verbose_name="Začátek", default=datetime.date.today)
    end = models.DateField(verbose_name="Konec", default=datetime.date.today)
    lector = models.ManyToManyField(Lector, verbose_name="Lektor/Lektoři")
    contact = models.CharField(verbose_name="Kontakt", max_length=100)
    description = models.TextField(verbose_name="Popis")
    image = models.ImageField(verbose_name="Obrázek", upload_to='images/')
    price = models.CharField(verbose_name="Cena (nepovinné)", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title

class EventLector(models.Model):
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    lectorId = models.ForeignKey(Lector, on_delete=models.CASCADE)
    class Meta:
     constraints = [
          models.UniqueConstraint(fields=['eventId', 'lectorId'], name='un_eventlector')
    ]
     

