from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Board(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    
    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name
    


class Card(models.Model):
    STATUS_OPTIONS = (
        ('To-do', 'To-do'),
        ('Doing', 'Doing'),
        ('Done', 'Done'),
    )

    PRIORITY_OPTIONS = (
        ('Low', 'Low'),
        ('Mid', 'Mid'),
        ('High', 'High'),
    )

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True) #title
    description = models.TextField(blank=True, null=True)   #desc
    estimate = models.DateField(blank=True, null=True)  #est
    priority = models.CharField(max_length=50, null=True, choices=PRIORITY_OPTIONS) 
    status = models.CharField(max_length=50, choices=STATUS_OPTIONS)

    updated = models.DateTimeField(auto_now=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-updated', '-created']
    
    def __str__(self):
        return self.name