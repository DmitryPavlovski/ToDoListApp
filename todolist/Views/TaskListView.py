from django.shortcuts import redirect, render
from todolist.models import Task
from todolist.forms import UpdateTaskForm
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

class TaskListView(LoginRequiredMixin, View):
    success_url = 'index'
    template_name = "index.html"
    form = UpdateTaskForm

    def post(self, request, *args, **kwargs):
        self.form = self.form(request.POST)
        if self.form.is_valid():
            task = self.form.save(commit=False)
            task.userId = request.user
            task.save()
            return redirect(self.success_url)
        else:
            return HttpResponse(str(form.errors))

    def get(self, request, *args, **kwargs):
        form = UpdateTaskForm()
        tasks = Task.objects.filter(
            userId=request.user).order_by('completed', '-created')
        return render(request, self.template_name, {"form": form, "tasks": tasks})

            
        