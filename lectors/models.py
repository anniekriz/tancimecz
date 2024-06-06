from django.db import models
from django.utils.text import slugify

# Create your models here.

class Lector(models.Model):
    name = models.CharField(max_length=100)  
    photo = models.ImageField(upload_to='images/')
    description = models.TextField()
    contact = models.CharField(max_length=100)
   
    def __str__(self):
        return self.name

    def beginning(self):
        # neukáže celý popis lektora hned na hlavní stránce, jenom 50 znaků
        return self.description[:100] + "..."