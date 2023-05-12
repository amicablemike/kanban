from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Board, Task
from .forms import BoardForm, TaskForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import User
from django.urls import reverse

# Create your views here.

def registerUser(request):
    page='register'

    if request.method == 'POST':
        username = request.POST['username'].lower()
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        try:
            if pass1 == pass2:
                myUser = User.objects.create_user(username, email, pass1)
                myUser.first_name = fname
                myUser.last_name = lname
                myUser.save()
                return redirect('login')
                
            else:
                return HttpResponse('Passwords dont match!')
        except:
            return HttpResponse('Bad Credentials!')
        

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def loginUser(request):
    page = 'login'

    if request.method =='POST':
        username = request.POST['username'].lower()
        pass1 = request.POST['pass1']

        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('ERROR: User does not exist!')
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('ERROR: Username and Password do not match!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def home(request):
    page = 'home'
    query = request.GET.get('q')
    
    #Search functionality
    if query:
        results = Board.objects.filter(name__icontains=query)
        boards = results
        try:
            myboards = results.filter(participants = request.user)
        except:
            myboards = ''   #if user is not loged in
    else:
        boards = Board.objects.all() 
        try:
            myboards = Board.objects.filter(participants = request.user)
        except:
            myboards = ''   #if user is not loged in
        
    context = {'page': page, 'boards': boards, 'myboards': myboards, 'board':board} 
    return render(request, 'base/home.html', context)


def createBoard(request):
    page = 'create-board'
    form = BoardForm

    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            form.save()
            board.participants.add(request.user)
            return redirect('home')
        else:
            return HttpResponse('ERROR: invalid form - action unsuccessful!')
        
    context = {'page': page, 'form': form}
    return render(request, 'base/board_form.html', context)


def board(request, pk):
    page = 'board'
    board = Board.objects.get(id=pk)
    participants = board.participants.all()
    query = request.GET.get('q2')   #Search functionality über URL query
    
    if query:
        tasks_todo = tasks_todo.filter(name__icontains=query)
        tasks_doing = tasks_doing.filter(name__icontains=query)
        tasks_done = tasks_done.filter(name__icontains=query)
    else:
        tasks_todo = Task.objects.filter(board = pk, status = 'To-do')
        tasks_doing = Task.objects.filter(board = pk, status = 'Doing')
        tasks_done = Task.objects.filter(board = pk, status = 'Done')
    
    try:
        user_tasks = Task.objects.filter(owner = request.user)  
    except:
        user_tasks = "" #if user is not loged in

    context = {'page': page, 'board': board, 'participants': participants, 'tasks_todo': tasks_todo, 'tasks_doing': tasks_doing, 'tasks_done': tasks_done,
                'user_tasks': user_tasks}
    return render(request, 'base/board.html', context)


def updateBoard(request, pk):
    page = 'update-board'
    board = Board.objects.get(id=pk)
    form = BoardForm(instance=board)
    

    if request.method == 'POST':
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            form.save()
            
            board.participants.add(request.user)
            board_url = reverse('board', args=[pk])
            return redirect(board_url)
        else:
            return HttpResponse('ERROR: invalid form - action unsuccessful!')

            # FEHLERMELDUNG !!
        

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

    #delete board if no participant exists
    if not board.participants.exists():
        board.delete()

    return redirect('home')


def createCard(request, pk):
    page = 'create-card'
    board = Board.objects.get(id=pk)
    form = TaskForm

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user   # loged in user becomes owner
            task.board = board          # active board 
            form.save()

            board.participants.add(request.user)
            board_url = reverse('board', args=[pk])
            return redirect(board_url)
        else:
            return HttpResponse('ERROR: invalid form - action unsuccessful!')

    context = {'page': page, 'form': form, 'board': board}
    return render(request, 'base/card_form.html', context)


def updateCard(request, pk):
    page = 'update-card'
    task = Task.objects.get(id = pk)
    board = task.board
    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            
            board.participants.add(request.user)
            board_url = reverse('board', args=[board.id])
            return redirect(board_url)
        else:
            return HttpResponse('ERROR: invalid form - action unsuccessful!')
        
    context = {'page': page, 'form': form, 'board': board, 'task':task}
    return render(request, 'base/card_form.html', context)


def deleteCard(request, pk):
    page = 'delete-card'
    task = Task.objects.get(id=pk)
    board = task.board
    board_url = reverse('board', args=[board.id])

    if request.user != task.owner and request.user != board.owner:
        return HttpResponse('You are not allowed to do that!')
    
    if request.method == 'POST':
        task.delete()
        return redirect(board_url)
    
    
    context = {'page': page,'task': task, 'board': board} 
    return render(request, 'base/delete_item.html', context)