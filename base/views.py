from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Board, Task
from .forms import BoardForm, TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
from django.urls import reverse

# Create your views here.

def loginPage(request):

    page = 'login'

    if request.method =='POST':
        username = request.POST['username'].lower()
        pass1 = request.POST['pass1']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist.')
        
        user = authenticate(request, username=username, password=pass1)

        if user is not None:
            login(request, user)
            # fname = user.first_name

            return redirect('home')
        else:
            messages.error(request, 'Username and Password do not match.')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page='register'

    if request.method == 'POST':
        username = request.POST['username'].lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myUser = User.objects.create_user(username, email, pass1)
        myUser.first_name = fname
        myUser.last_name = lname

        myUser.save()

        messages.success(request, "Your Account has been created successfully.")

        return redirect('login')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def home(request):
    query = request.GET.get('q')
    page = 'home'
    if query:
        results = Board.objects.filter(name__icontains=query)
        boards = results
        try:
            myboards = results.filter(participants = request.user)
        except:
            myboards = Board.objects.all()  #warum try except?? - testen ohne try except
    else:
        boards = Board.objects.all() 
        try:
            myboards = Board.objects.filter(participants = request.user)
        except:
            myboards = Board.objects.all()  #error umgehen, wenn user nicht angemeldet
        
    context = {'page': page, 'boards': boards, 'myboards': myboards, 'board':board} 
    return render(request, 'base/home.html', context)


def board(request, pk):
    page = 'board'
    board = Board.objects.get(id=pk)
    participants = board.participants.all()
    tasks_todo = Task.objects.filter(board = pk, status = 'To-do')
    tasks_doing = Task.objects.filter(board = pk, status = 'Doing')
    tasks_done = Task.objects.filter(board = pk, status = 'Done')
    

    #Search functionality über URL query
    query = request.GET.get('q')
    if query:
        tasks_todo = tasks_todo.filter(name__icontains=query)
        tasks_doing = tasks_doing.filter(name__icontains=query)
        tasks_done = tasks_done.filter(name__icontains=query)
    
    try:
        user_tasks = Task.objects.filter(owner = request.user)  
    except:
        user_tasks = "" # darf nicht None sein, falls user nicht eingelogged

    context = {'page': page, 'board': board, 'participants': participants, 'tasks_todo': tasks_todo, 'tasks_doing': tasks_doing, 'tasks_done': tasks_done,
                'user_tasks': user_tasks}
    return render(request, 'base/board.html', context)

@login_required(login_url='login')
def createBoard(request):
    page = 'create-board'
    form = BoardForm
    creator = request.user

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            form.save()
            board.participants.add(request.user)
            return redirect('home')
        else:
            form = BoardForm
            return redirect('home')
        
    context = {'page': page, 'creator':creator, 'form': form}
    return render(request, 'base/board_form.html', context)

def updateBoard(request, pk):
    page = 'update-board'
    board = Board.objects.get(id=pk)
    form = BoardForm(instance=board)
    board_url = reverse('board', args=[board.id])

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            #task.owner = request.user  # den eingeloggten User als owner des Tasks setzen
            #task.board = board
            form.save()
            
            board.participants.add(request.user)
            return redirect(board_url)
        else:
            form = BoardForm(request.POST, instance=board)
            return redirect('home')
        

    context = {'page': page, 'board':board, 'form':form}
    return render(request, 'base/board_form.html', context)

def deleteBoard(request, pk):
    page = 'delete-board'
    board = Board.objects.get(id=pk)

    if request.user != board.owner:
        return HttpResponse('You are not allowed to do that!')
    
    if request.method == 'POST':
        board.delete()
        return redirect('home')
    
    
    context = {'board': board, 'page': page} 
    return render(request, 'base/delete_item.html', context)

def leaveBoard(request, pk):
    board = Board.objects.get(id = pk)
    board.participants.remove(request.user)
    return redirect('home')

def createCard(request, pk):
    page = 'create-card'
    board = Board.objects.get(id=pk)
    form = TaskForm
    creator = request.user

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user  # den eingeloggten User als owner des Tasks setzen
            task.board = board
            form.save()

            board.participants.add(request.user)
            
            board_url = reverse('board', args=[pk])
            return redirect(board_url)
        else:
            form = TaskForm()

    context = {'page': page, 'form': form, 'board': board, 'creator': creator}
    return render(request, 'base/card_form.html', context)

def updateCard(request, pk):
    page = 'update-card'
    task = Task.objects.get(id = pk)
    board = task.board
    form = TaskForm(instance=task)
    board_url = reverse('board', args=[board.id])
    creator = request.user


    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        print()
            # do something with the form data
        if form.is_valid():
            task = form.save(commit=False)
            #task.owner = request.user  # den eingeloggten User als owner des Tasks setzen
            #task.board = board
            form.save()
            
            board.participants.add(request.user)
            
            #board_url = reverse('board', args=[pk])
            return redirect(board_url)
        else:
            form = TaskForm(request.POST, instance=task)
            return redirect('home')
        
    context = {'page': page, 'form': form, 'board': board, 'task':task, 'creator': creator}
    return render(request, 'base/card_form.html', context)

def deleteCard(request, pk):
    page = 'delete-card'
    task = Task.objects.get(id=pk)
    board = task.board
    board_url = reverse('board', args=[board.id])

    if request.user != task.owner:
        return HttpResponse('You are not allowed to do that!')
    
    if request.method == 'POST':
        task.delete()
        return redirect(board_url)
    
    
    context = {'page': page,'task': task, 'board': board} 
    return render(request, 'base/delete_item.html', context)