from django.http import HttpResponse
from django.views import generic
from django.db.models import Avg, Value, F, Count, Sum
from django.db.models.functions import ExtractWeek, TruncWeek
from .models import Entry
import datetime

class IndexView(generic.ListView):

    def get_queryset(self):
        
        #filter by user
        avg_speed = Entry.objects.filter(user=self.request.user).aggregate(Avg('speed'))
        entries =  Entry.objects.filter(user=self.request.user).values('datetime', 'distance', 'duration')
        entries_data = {**avg_speed, 'entries': entries}
        print(entries_data)
        return entries

class Weekly(generic.ListView):
    template_name = 'statistic/weekly.html'

    def get_queryset(self):
        #filter by user
        end_datetime = datetime.datetime.utcnow()
        start_datetime = end_datetime - datetime.timedelta(days=365)
        entries = Entry.objects.filter(user=self.request.user, datetime__range=(start_datetime, end_datetime)).annotate(week=ExtractWeek('datetime')).values(
            'week').annotate(avg_speed=Avg('speed'), total_distance=Sum('distance'), total_duration=Sum('duration'), total_entries=Count('id'))
        print(entries)
        return entries