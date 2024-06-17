from django.db import models
import datetime

# Create your models here.

# pokaždé když přidám model nebo udělám v nějakém změnu udělám:
# python manage.py makemigrations
# python manage.py migrate
 
class Event(models.Model):
  title = models.CharField(max_length=100)
  link = models.CharField(max_length=200, null=True, blank=True)
  date_time = models.DateTimeField("DateTime", default=datetime.datetime.now)
  #date = models.DateField(("Date"), default=datetime.date.today)
  #time = models.TimeField(("Time"), default=lambda: datetime.datetime.now().time())
  town = models.CharField(max_length=100)
  adress = models.CharField(max_length=100)
  lector = models.CharField(max_length=100)
  contact = models.CharField(max_length=100)
  description = models.TextField()

  # jak bude event (instance Event) vypadat z venku - když chci zobrazit objekty nechci jen: Event object, ale chci, aby měli název - to zařídí tahle funkce
  def __str__(self):
    return self.title
    # = string version of that event

