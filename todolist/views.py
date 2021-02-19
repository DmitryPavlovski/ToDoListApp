from django.shortcuts import render, HttpResponse, redirect
from django.http import Http404
from .forms import CreateTaskForm, UpdateTaskForm, RegistrForm
from django.contrib.auth import authenticate, login
from .models import Task
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

