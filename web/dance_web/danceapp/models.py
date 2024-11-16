from django.db import models
import datetime
from django.contrib.auth.models import User

class Lector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Uživatel")
    firstName = models.CharField(max_length=50, verbose_name="Jméno")
    lastName = models.CharField(max_length=50, null=True, blank=True, verbose_name="Příjmení")
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True, verbose_name="Fotka")
    description = models.TextField(verbose_name="Popis")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="Telefon")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    link = models.CharField(max_length=256, null=True, blank=True, verbose_name="Odkaz na stránku")

    class Meta:
        ordering = ['firstName'] #řazení lektorů podle abecedy
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
    lector = models.ForeignKey('Lector', on_delete=models.PROTECT, verbose_name="Lektor")

    def __str__(self):
        return f"{self.town}, {self.address}"
    
    class Meta:
        verbose_name = "Místo konání"
        verbose_name_plural = "Místa konání"

class EventGroup(models.Model):
    lector = models.ManyToManyField(Lector, verbose_name="Lektor")
    location = models.ForeignKey(Location, verbose_name="Místo konání", on_delete=models.PROTECT)
    startTime = models.TimeField(verbose_name="Začátek", default='18:00')
    endTime = models.TimeField(verbose_name="Konec (nepovinné)", default='20:00', null=True, blank=True)
    description = models.TextField(verbose_name="Popis")
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

    def short_description(self):
        return self.description[:75] + '...' if len(self.description) > 75 else self.description

class Event(models.Model):
    parent = models.ForeignKey(EventGroup, verbose_name="Event Group", on_delete=models.PROTECT)
    date = models.DateField(verbose_name="Datum", default=datetime.date.today)
    description = models.TextField(verbose_name="Dodatečný popis (nepovinné)", null=True, blank=True)

    town_to_number = {}
    next_number = 1

    def __str__(self):
        startTime = self.parent.startTime.strftime('%H:%M')
        endTime = self.parent.endTime.strftime('%H:%M') if self.parent.endTime else 'N/A'
        date = self.date.strftime('%d.%m. %Y')
        if self.parent.endTime:
            return f"{self.parent.location.town} {date} {startTime}-{endTime}"
        return f"{self.parent.location.town} {date} {startTime}"
    
    class Meta:
        verbose_name = "Taneční večer"
        verbose_name_plural = "Taneční večery"
    
    @property
    def endTime(self):
        return self.parent.endTime
    
    @property
    def colorNumber(self):
        town_name = self.parent.location.town
        
        if town_name not in Event.town_to_number:
            Event.town_to_number[town_name] = Event.next_number
            Event.next_number = (Event.next_number % 6) + 1
        
        return Event.town_to_number[town_name]

class Workshop(models.Model):
    title = models.CharField(verbose_name="Název", max_length=101)
    link = models.CharField(verbose_name="Odkaz (nepovinné)", max_length=256, null=True, blank=True)
    location = models.ForeignKey(Location, verbose_name="Místo konání", on_delete=models.PROTECT)
    start = models.DateField(verbose_name="Začátek", default=datetime.date.today)
    end = models.DateField(verbose_name="Konec", default=datetime.date.today)
    startTime = models.TimeField(verbose_name="Začátek (nepovinné)", default='18:00',null=True, blank=True)
    endTime = models.TimeField(verbose_name="Konec (nepovinné)", default='20:00', null=True, blank=True)
    lector = models.ManyToManyField(Lector, verbose_name="Lektor/Lektoři")
    description = models.TextField(verbose_name="Popis")
    image = models.ImageField(verbose_name="Obrázek", upload_to='images/')
    price = models.CharField(verbose_name="Cena (nepovinné)", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Workshop"
        verbose_name_plural = "Workshopy"

class EventLector(models.Model):
    eventId = models.ForeignKey(Event, on_delete=models.CASCADE)
    lectorId = models.ForeignKey(Lector, on_delete=models.CASCADE)
    class Meta:
     constraints = [
          models.UniqueConstraint(fields=['eventId', 'lectorId'], name='un_eventlector')
    ]
     

