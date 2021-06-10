from django.urls import path

from . import views

urlpatterns = [
    path('', views.create_entry, name='index'),
    path('weekly/', views.Weekly.as_view(), name='weekly_entry_statistic'),
    path('entry_detail/<int:id>/', views.get_entry, name='entry_detail'),
    path('delete/<int:id>', views.delete_entry, name='delete'),
]