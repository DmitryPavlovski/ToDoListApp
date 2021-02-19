from todolist.forms import RegistrForm
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect


class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/sign_up.html'
    success_url = "/index"
    form_class = RegistrForm
    success_message = "Your profile was created successfully"

    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
        login(self.request, user)
        return redirect(self.success_url)