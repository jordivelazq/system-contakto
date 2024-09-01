

from app.core.models import UserManager, User
from app.core.forms.user_manager import UserManagerForm
from django.views.generic import CreateView, DeleteView
from django.contrib import messages
from django.urls import reverse_lazy


class UserManagerView(CreateView):
    model = UserManager
    form_class = UserManagerForm
    template_name = "core/user_manager/UserManagerForm.html"
    
    def get_context_data(self, **kwargs):
        context = super(UserManagerView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.main = self.request.user
        form.save()
        messages.success(self.request, "El usuario ha sido copiado con éxito.")
        return super(UserManagerView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(UserManagerView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')


class UserManagerDeleteView(DeleteView):
    model = UserManager
    template_name = "core/user_manager/UserManagerFormDelete.html"

    def get_context_data(self, **kwargs):
        context = super(UserManagerDeleteView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        messages.success(self.request, "Usuario desactivado con éxito.")
        return super(UserManagerDeleteView, self).form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super(UserManagerDeleteView, self).form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('core:user-manager-add')