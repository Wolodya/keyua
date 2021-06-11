from django.http import HttpResponse
from django.views import generic
from django.db.models import Avg, Count, Sum
from django.db.models.functions import ExtractWeek
from .models import Entry
from .forms import CreateEntryForm, FilterForm
import datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def weekly_stats(request):
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(days=365)
    entries = Entry.stats.get_weekly_stats(start_datetime,end_datetime,request.user)
    context={'stats':entries}
    return render(request, 'statistic/weekly.html', context)


@login_required
def create_entry(request):
    if request.method == 'POST':
        entry = Entry(user=request.user)
        form = CreateEntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry.save()
            form = CreateEntryForm()
            messages.info(request, 'Successful create')
    else:
        form = CreateEntryForm()
    context = {'form':form}
    return render(request, 'statistic/entry_create.html', context)

@login_required
def get_entry(request, **kwargs):
    entry_id = kwargs.get('id')
    entry = get_object_or_404(Entry, pk=entry_id)

    if request.method == "POST":
        form = CreateEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.info(request, 'Successful update')
    else:
        form = CreateEntryForm(instance=entry)

    context = {'entry':entry, 'form': form}
    return render(request, 'statistic/entry_detail.html', context )

@login_required
def delete_entry(request, **kwargs):
    entry_id = kwargs.get('id')
    entry = Entry.objects.get(id=entry_id)
    entry.delete()
    messages.info(request, 'Successful delete')
    return redirect('statistic:index')

@login_required
def entry_list(request, **kwargs):
    form = FilterForm(request.POST)
    qs = None
    if form.is_valid():
        datetime_start=form.cleaned_data['datetime_start']
        datetime_end=form.cleaned_data['datetime_end']
        qs =  Entry.objects.filter(user=request.user, datetime__range=(datetime_start, datetime_end))
    else:
        qs =  Entry.objects.filter(user=request.user)
    avg_speed = qs.aggregate(Avg('speed'))['speed__avg']
    avg_speed = avg_speed and round(avg_speed, 2)
    entries = qs.values('id','datetime','distance','duration')
    
    context = {'entries': entries, 'avg_speed': avg_speed, 'form':form}
    return render(request, 'statistic/entry_list.html', context)