# from django.utils import timezone
from django.forms import ModelForm
from .models import Board, Card
from django import forms
from django.forms.widgets import DateInput

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description')

class CardForm(ModelForm):
    estimate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Card
        fields = ('name', 'description', 'priority', 'status', 'estimate')