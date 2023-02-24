from django.forms import ModelForm
from .models import Board, Task

class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = '__all__'

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'