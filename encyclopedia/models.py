from django.db import models
from django.db.models.fields import CharField, TextField

# Create your models here.
class Entry(models.Model):
    title = CharField(max_length=120)
    content = TextField(blank=True)

