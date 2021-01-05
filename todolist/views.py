from django.shortcuts import render, HttpResponse, redirect
from .forms import TaskForm
from .models import Task

# Create your views here.

def main(request):
    return render(request, "base.html")

def index(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
    tasks = Task.objects.all()
    return render(request, "index.html", {"task_form": form, "tasks": tasks})
