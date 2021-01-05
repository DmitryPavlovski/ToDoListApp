from django import forms
from django.forms import ModelForm
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        #fields = "__all__"  # include all fields in form
        fields=('title', 'description', 'userId')