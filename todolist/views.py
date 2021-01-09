from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from .forms import TaskForm
from .models import Task

# Create your views here.

def main(request):
    if request.user.is_authenticated:
        return show_index(request)
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
        form.save()
        return redirect("index")

def show_index(request):
    form = TaskForm()
    tasks = Task.objects.filter(userId = request.user)
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
        form = TaskForm(instance=task)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
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