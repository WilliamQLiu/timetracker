from django.db import models

# Create your models here.

class Text(models.Model):
    """ Text data """
    temp = models.CharField(max_length=128) # Source of text
    texttime = models.DateTimeField() # When text occurred
    month = models.CharField(max_length=3)
    time = models.TimeField()
    textnumber = models.IntegerField() # Phone Number
    data = models.TextField() # Actual text

