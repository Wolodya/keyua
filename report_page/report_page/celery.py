from django.conf import settings
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'report_page.settings')

app = Celery('report_page')


app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
    worker_preftch_multiplier=1,
    tasks_acks_late=True,
    task_ignore_result=True,
    task_store_errors_even_if_ignored=True
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
