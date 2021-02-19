from todolist.forms import UpdateTaskForm
from todolist.models import Task
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = UpdateTaskForm
    template_name = 'update_task.html'
    success_url = '/index'
