from django.urls import path

from . import views

app_name = 'statistic'

urlpatterns = [
    path('', views.entry_list, name='index'),
    path('create/', views.create_entry, name='create_entry'),
    path('entry_detail/<int:id>/', views.get_entry, name='entry_detail'),
    path('delete/<int:id>', views.delete_entry, name='delete'),
    path('weekly/', views.weekly_stats, name='weekly'),
]