from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from .forms import TaskForm, RegistrForm
from .models import Task
from django.contrib.auth import authenticate, login

# Create your views here.

def main(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        return redirect("login")

def index(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return show_index(request)
        elif request.method == "POST":
            return new(request)
    else:
        return redirect('main')      

def new(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.userId = request.user
        task.save()
        return redirect("index")
    else:
        return HttpResponse(str(form.errors))

def show_index(request):
    form = TaskForm()
    tasks = Task.objects.filter(userId = request.user).order_by('completed', '-created')
    return render(request, "index.html", {"task_form": form, "tasks": tasks})

def update_task(request, pk):
    if request.user.is_authenticated:
        if request.method == "GET":
            return show_update_task(request, pk)
        if request.method == "POST":
            return save_updated_task(request, pk)
    else:
        raise Http404("Task not found.")

def save_updated_task(request, pk):
    task = Task.objects.get(id=pk)
    if task.userId == request.user:
        form = TaskForm(request.POST)
        if form.is_valid():
            task.completed = form.cleaned_data['completed']
            task.description = form.cleaned_data['description']
            task.title = form.cleaned_data['title']
            task.save()
            return redirect("index")
    else:
        raise Http404("Task not found.")

def show_update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    
    return render(request, "update_task.html", {"task_edit_form": form})

def delete_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(id=pk)
        if task.userId == request.user:
            task.delete()
            return redirect("index")
    raise Http404("Task not found.")

def complate_task(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(id=pk)
        if task.userId == request.user:
            task.completed = not task.completed
            task.save()
            return redirect("index")
    raise Http404("Task not found.")

def sign_up(request):
    data = {}
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect("index")
        else:
            data['form'] = form
            return render(request, 'registration/sign_up.html', data)
    else:
        form = RegistrForm()
        data['form'] = form
        return render(request, 'registration/sign_up.html', data)