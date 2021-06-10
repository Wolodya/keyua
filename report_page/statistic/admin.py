from django.contrib import admin
# Register your models here.

from .models import Entry

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ['speed']