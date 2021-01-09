from django.shortcuts import render, HttpResponse, redirect
from .forms import TaskForm
from .models import Task

# Create your views here.

def main(request):
    if request.user.is_authenticated:
        return render(request, "base.html")
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
    tasks = Task.objects.all()
    return render(request, "index.html", {"task_form": form, "tasks": tasks})

def update_task(request, pk):    
    if request.method == "GET":
        return show_update_task(request, pk)
    if request.method == "POST":
        return save_updated_task(request, pk)

def save_updated_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    form = TaskForm(request.POST, instance=task)
    if form.is_valid():
        form.save()
        return redirect("index")

def show_update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    return render(request, "update_task.html", {"task_edit_form": form})

def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect("index")