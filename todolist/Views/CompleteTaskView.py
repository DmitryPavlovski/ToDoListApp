from django.shortcuts import redirect
from django.http import Http404
from todolist.models import Task
from django.views.generic.edit import View
from django.contrib.auth.mixins import LoginRequiredMixin

class CompleteTaskView(LoginRequiredMixin, View):
    success_url = 'index'

    def get(self, request, pk, *args, **kwargs):
        task = Task.objects.get(id=pk)
        if task.userId == request.user:
            task.completed = not task.completed
            task.save()
            return redirect(self.success_url)
        raise Http404("Task not found.")
            
        