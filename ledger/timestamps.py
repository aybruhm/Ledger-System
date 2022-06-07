from django.db import models


class TimeStampModel(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True
        verbose_name_plural = "Time Stamps"