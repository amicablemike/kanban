# from django.utils import timezone
from django.forms import ModelForm
from .models import Board, Task
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

class TaskForm(ModelForm):
    #board_id = forms.IntegerField(widget=forms.HiddenInput())
    estimate = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'status', 'estimate')

    # def save(self, commit=True):
    #     task = super().save(commit=False)
    #     task.created = timezone.now()  # set the created field
    #     if commit:
    #         task.save()
    #     return task


