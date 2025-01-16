from django.db import models
import datetime
from django.contrib.auth.models import User
from threading import Lock
from django.core.exceptions import ValidationError


class OrderedLectorManager(models.Manager):
    def get_queryset(self):
        # Order by EventLector.order
        return super().get_queryset().order_by('eventlector__order')


class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Uživatel")
    firstName = models.CharField(max_length=50, verbose_name="Jméno")
    lastName = models.CharField(max_length=50, null=True, blank=True, verbose_name="Příjmení")
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', verbose_name="Fotka")
    description = models.TextField(verbose_name="Popis")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telefon")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    link = models.CharField(max_length=256, null=True, blank=True, verbose_name="Odkaz na stránku")
    fb = models.CharField(max_length=256, null=True, blank=True, verbose_name="Facebook")

    objects = models.Manager()  # Default manager
    ordered_objects = OrderedLectorManager()  # Custom manager for ordering

    class Meta:
        verbose_name = "Lektor"
        verbose_name_plural = "Lektoři"

    def __str__(self):
        return f"{self.firstName} {self.lastName or ''}".strip()
    
class Location(models.Model):
    coordinates = models.CharField(max_length=50, verbose_name="Souřadnice")
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name="Název místa (nepovinné)")
    town = models.CharField(max_length=50, verbose_name="Město/Obec")
    address = models.CharField(max_length=100, verbose_name="Adresa (ulice a ČP)")
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name="Popis (jak se k nám dostat)")
    lector = models.ManyToManyField(Lector, verbose_name="Lektor")

    def __str__(self):
        return f"{self.town}, {self.address}"
    
    class Meta:
        verbose_name = "Místo konání"
        verbose_name_plural = "Místa konání"

class EventGroup(models.Model):
    lector = models.ManyToManyField(Lector, through='EventLector', verbose_name="Lektor")
    location = models.ForeignKey(Location, verbose_name="Místo konání", on_delete=models.PROTECT)
    startTime = models.TimeField(verbose_name="Začátek", default='18:00')
    endTime = models.TimeField(verbose_name="Konec (nepovinné)", default='20:00', null=True, blank=True)
    description = models.TextField(verbose_name="Popis (nepovinné)", null=True, blank=True)
    image = models.ImageField(verbose_name="Obrázek", upload_to='images/', null=True, blank=True)

    def __str__(self):
        startTime = self.startTime.strftime('%H:%M')
        endTime = self.endTime.strftime('%H:%M') if self.endTime else 'N/A'
        if self.endTime:
            return f"{self.location.town} {startTime}-{endTime}"
        return f"{self.location.town} {startTime}"
    
    class Meta:
        verbose_name = "Taneční večer"
        verbose_name_plural = "Taneční večery"
        ordering = ['-startTime']

    def short_description(self):
        return self.description[:75] + '...' if len(self.description) > 75 else self.description
    
    @property
    def ordered_lectors(self):
        # Fetch lectors via EventLector and order them by `EventLector.order`
        return Lector.objects.filter(eventlector__eventId=self).order_by('eventlector__order')

class Event(models.Model):
    parent = models.ForeignKey('EventGroup', verbose_name="Event Group", on_delete=models.PROTECT)
    date = models.DateField(verbose_name="Datum", default=datetime.date.today)
    description = models.TextField(verbose_name="Dodatečný popis (nepovinné)", null=True, blank=True)

    _lock = Lock()
    town_to_number = {}
    next_number = 1

    def __str__(self):
        if not self.parent:
            return f"Event on {self.date.strftime('%d.%m.%Y')}"
        startTime = self.parent.startTime.strftime('%H:%M') if self.parent.startTime else 'N/A'
        endTime = self.parent.endTime.strftime('%H:%M') if self.parent.endTime else 'N/A'
        date = self.date.strftime('%d.%m. %Y')
        return f"{self.parent.location.town} {date} {startTime}-{endTime}" if self.parent.endTime else f"{self.parent.location.town} {date} {startTime}"
    
    class Meta:
        verbose_name = "Taneční večer"
        verbose_name_plural = "Taneční večery"
        ordering = ['-date']
    
    @property
    def endTime(self):
        return self.parent.endTime
    
    @property
    def colorNumber(self):
        town_name = self.parent.location.town
        with Event._lock:
            if town_name not in Event.town_to_number:
                Event.town_to_number[town_name] = Event.next_number
                Event.next_number = (Event.next_number % 6) + 1
        return Event.town_to_number[town_name]


class Workshop(models.Model):
    title = models.CharField(verbose_name="Název - 1. řádek", max_length=101)
    title2 = models.CharField(verbose_name="Název - 2. řádek (nepovinné)", max_length=101, null=True, blank=True)
    link = models.CharField(verbose_name="Odkaz (nepovinné)", max_length=256, null=True, blank=True)
    location = models.ForeignKey('Location', verbose_name="Místo konání", on_delete=models.PROTECT)
    start = models.DateField(verbose_name="Začátek", default=datetime.date.today)
    end = models.DateField(verbose_name="Konec", default=datetime.date.today)
    startTime = models.TimeField(verbose_name="Začátek (nepovinné)", null=True, blank=True, default=None)
    endTime = models.TimeField(verbose_name="Konec (nepovinné)", null=True, blank=True, default=None)
    lector = models.ManyToManyField('Lector', verbose_name="Lektor/Lektoři")
    description = models.TextField(verbose_name="Popis")
    image = models.ImageField(verbose_name="Obrázek", upload_to='images/', null=True, blank=True)
    price = models.CharField(verbose_name="Cena (nepovinné)", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshopy"
        ordering = ['-start']

    def clean(self):
        super().clean()
        if self.start > self.end:
            raise ValidationError("The start date cannot be later than the end date.")

class EventLector(models.Model):
    eventId = models.ForeignKey(EventGroup, on_delete=models.CASCADE)
    lectorId = models.ForeignKey(Lector, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(verbose_name="Pořadí", default=0)

    class Meta:
        verbose_name = "Lektor"
        verbose_name_plural = "Lektoři"
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['eventId', 'lectorId'], name='un_eventlector')
        ]

    # def clean(self):
    #     # Ensure order values are unique within the same EventGroup
    #     if EventLector.objects.filter(eventId=self.eventId, order=self.order).exclude(pk=self.pk).exists():
    #         raise ValidationError(f"Číslo {self.order} už má jiný lektor")
     

