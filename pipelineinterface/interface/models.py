from django.db import models

# Create your models here.
class celeryResponse(models.Model):
    output=  models.TextField(max_length = 255, unique = False)
