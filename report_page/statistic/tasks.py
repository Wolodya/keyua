from celery import Task
from django.core.mail import send_mail
from django.conf import settings
from report_page.celery import app
from django.contrib.auth.models import User
from .models import Entry
import datetime
import json


class UserSelection(Task):
    name = 'select users'
    max_retries = 3
    soft_time_limit = 120

    def run(self, *args, **kwargs):
        recievers = User.objects.filter(is_staff=False).values('email','id')
        for user in recievers:
            params = {'email':user['email'],'user':user['id']}
            StatsSending().delay(**params)


class StatsSending(Task):
    name = "Sending weekly stats to user"
    max_retries = 3
    soft_time_limit = 120

    def run(self, *args, **kwargs):
        email = kwargs.get('email', None)
        user = kwargs.get('user', None)
        if not user:
            return
        end_datetime = datetime.datetime.utcnow()
        start_datetime = end_datetime - datetime.timedelta(days=365)
        entries = Entry.stats.get_weekly_stats(start_datetime,end_datetime,user).values('week','avg_speed','total_distance','total_duration','total_entries')
        subject = f'Your weekly statistic'
        message = json.dumps(list(entries))
        email_from = 'admin@admin.com'
        recipient_list = [email]

        send_mail( subject, message, email_from, recipient_list )

user_selection = app.register_task(UserSelection())
stats_sending = app.register_task(StatsSending())