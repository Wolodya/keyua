from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractWeek

class EntryManager(models.Manager):
    def get_weekly_stats(self, start_datetime, end_datetime, user):
        return self.filter(user=user, datetime__range=(start_datetime, end_datetime)).annotate(week=ExtractWeek('datetime')).values(
            'week').annotate(avg_speed=Avg('speed'), total_distance=Sum('distance'), total_duration=Sum('duration'), total_entries=Count('id'))


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

    stats = EntryManager()