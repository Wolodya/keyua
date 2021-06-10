from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Entry(models.Model):
    datetime = models.DateTimeField()
    distance = models.FloatField(db_index=True)
    duration = models.FloatField(db_index=True)
    speed = models.FloatField(db_index=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)+str(self.distance)+str(self.duration)+str(self.datetime)

    def save(self, *args, **kwargs):
        self.speed = self.distance/self.duration
        super().save(*args,**kwargs)