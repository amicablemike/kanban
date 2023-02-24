from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Board, Task, Comment
from .forms import BoardForm, TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    boards = Board.objects.all()
    
    board_count = boards.count()
    
    context = {'boards': boards, 'board_count': board_count} 
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.method =='POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist.')


    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # saving form, freeze in time, acces created user right away, getting user object -> in order to clean data
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration.')


    return render(request, 'base/sign_up.html', {'form': form})


def board(request, pk):
    board = Board.objects.get(id=pk)
    participants = board.participants.all()

    context = {'board': board, 'participants': participants}
    return render(request, 'base/board.html', context)

@login_required(login_url='login')
def createBoard(request):
    form = BoardForm()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')