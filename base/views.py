from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
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
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # board = Board.objects.filter(
    #     Q(name__icontains=q) |
    #     Q(description__icontains=q)
    # )

    boards = Board.objects.all()[:]
    try:
        myboards = Board.objects.filter(participants = request.user)[:]
    except:
        myboards = Board.objects.filter()[:]
    
    board_count = boards.count()
    


    context = {'boards': boards, 'myboards': myboards, 'board':board, 'board_count': board_count} 
    return render(request, 'base/home.html', context)


def board(request, pk):
    board = Board.objects.get(id=pk)
    participants = board.participants.all()
    tasks_todo = Task.objects.filter(board = pk, status = 'To-do')
    tasks_doing = Task.objects.filter(board = pk, status = 'Doing')
    tasks_done = Task.objects.filter(board = pk, status = 'Done')
    task = Task.objects.filter(board = pk)
    
    task_form = TaskForm
    board_form = BoardForm

    user_tasks = Task.objects.filter(owner = request.user)  


    context = {'task_form': task_form, 'board': board, 'participants': participants, 'tasks_todo': tasks_todo, 'tasks_doing': tasks_doing, 'tasks_done': tasks_done,
                'user_tasks': user_tasks, 'task': task, 'board_form': board_form, 'task_form': task_form}
    return render(request, 'base/board.html', context)

@login_required(login_url='login')
def createBoard(request):
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
        
    context = {'creator':creator, 'form': form}
    return render(request, 'base/board_form.html', context)

def updateBoard(request, pk):
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
        

    context = {'board':board, 'form':form}
    return render(request, 'base/board_form.html', context)


def createCard(request, pk):
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

    context = {'form': form, 'board': board, 'creator': creator}
    return render(request, 'base/card_form.html', context)


def updateCard(request, pk):
   #board = Board.objects.get(id = pk)
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
        
    context = {'form': form, 'board': board, 'task':task, 'creator': creator}
    return render(request, 'base/card_form.html', context)