# from django.utils import timezone
from django.forms import ModelForm
from .models import Board, Card
from django import forms
from django.forms.widgets import DateInput

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ('name', 'description')

    # def save(self, commit=True):
    #     board = super().save(commit=False)
    #     board.created = timezone.now()  # set the created field
    #     if commit:
    #         board.save()
    #     return board

class CardForm(ModelForm):
    #board_id = forms.IntegerField(widget=forms.HiddenInput())
    estimate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Card
        fields = ('name', 'description', 'priority', 'status', 'estimate')

    # def save(self, commit=True):
    #     card = super().save(commit=False)
    #     card.created = timezone.now()  # set the created field
    #     if commit:
    #         card.save()
    #     return card


