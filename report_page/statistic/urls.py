from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='entry statistic'),
    path('weekly/', views.Weekly.as_view(), name='weekly entry statistic')
]