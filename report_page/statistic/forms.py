from django import forms
from django.db.models import fields
from .models import Entry

class CreateEntryForm(forms.ModelForm):
    distance = forms.FloatField(min_value=0.001)
    duration = forms.FloatField(min_value=0.001)

    class Meta:
        model = Entry
        exclude = ['speed', 'user']

class DateInput(forms.DateInput):
    input_type = 'date'

class FilterForm(forms.Form):
    datetime_start=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    datetime_end=forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))

    def clean_datetime_end(self):
        start_date = self.cleaned_data['datetime_start']
        end_date = self.cleaned_data['datetime_end']

        if end_date <= start_date:
            raise forms.ValidationError("End date must be later than start date")
        return end_date