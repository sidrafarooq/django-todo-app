from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError

from .forms import TodoForm
from .models import Todo

from django.utils import timezone

def signupuser(request):

    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {
            'form': UserCreationForm()
        })

    if request.POST['password1'] == request.POST['password2']:

        try:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)

            return redirect('currenttodos')

        except IntegrityError:
            return render(request, 'todo/signupuser.html', {
                'form': UserCreationForm(),
                'error': 'User already exists'
            })


    else:
        return render(request, 'todo/signupuser.html', {
            'form': UserCreationForm(),
            'error': 'Password and Confirm password dont match'
        })


def loginuser(request):

    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {
            'form': AuthenticationForm()
        })

    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

    if user is None:
        return render(request, 'todo/loginuser.html', {
            'form': AuthenticationForm(),
            'error': 'User and Password dont match'
        })
    else:
        login(request, user)
        return redirect('currenttodos')

def home(request):
    return render(request, 'todo/home.html')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {
        'todos': todos
    })


@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {
        'todos': todos
    })


@login_required
def createtodo(request):

    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {
            'form' : TodoForm()
        })

    try:
        form = TodoForm(request.POST)
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()

        return redirect('currenttodos')

    except ValueError:
        return render(request, 'todo/createtodo.html', {
            'form': TodoForm(),
            'error': 'Bad data passed'
        })


@login_required
def viewtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {
            'todo': todo,
            'form': form
        })

    try:
        form = TodoForm(request.POST, instance=todo)
        form.save()
        return redirect('currenttodos')

    except ValueError:
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {
            'todo': todo,
            'form': form,
            'error': 'bad data passed, try again'
        })


@login_required
def completedtodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.delete()
        return redirect('currenttodo')
