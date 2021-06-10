from django import forms
from django.db.models import fields
from .models import Entry

class CreateEntryForm(forms.ModelForm):

    class Meta:
        model = Entry
        exclude = ['speed']