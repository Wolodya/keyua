from django.http import HttpResponse
from django.views import generic
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractWeek
from .models import Entry
from .forms import CreateEntryForm
import datetime
from django.shortcuts import get_object_or_404, redirect, render

class IndexView(generic.ListView):

    def get_queryset(self):
        
        #filter by user
        avg_speed = Entry.objects.filter(user=self.request.user).aggregate(Avg('speed'))
        entries =  Entry.objects.filter(user=self.request.user).values('id','datetime', 'distance', 'duration')
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

def create_entry(request):
    if request.method == 'POST':
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            form.save()
            form = CreateEntryForm()
    else:
        form = CreateEntryForm()

    entries = Entry.objects.all().order_by('-datetime')
    context = {'form':form, 'entries': entries}
    return render(request, 'statistic/entry_list.html', context)

def get_entry(request, **kwargs):
    entry_id = kwargs.get('id')
    entry = get_object_or_404(Entry, pk=entry_id)

    if request.method == "POST":
        form = CreateEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
    else:
        form = CreateEntryForm(instance=entry)

    context = {'entry':entry, 'form': form}
    return render(request, 'statistic/entry_detail.html', context )

def delete_entry(request, **kwargs):
    entry_id = kwargs.get('id')
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    return redirect('index')