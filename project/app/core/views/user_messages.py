from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (DeleteView, DetailView, ListView,
                                  RedirectView, UpdateView)
from ..models import UserMessage


class UserMessajeListView(LoginRequiredMixin, ListView):

    model = UserMessage
    paginate_by = 25

    context_object_name = "user_messages"
    template_name = 'core/user_messages/user_messages_list.html'

    page = {
        'title': 'Users',
        'subtitle': 'messages'
    }

    def get_queryset(self):
        user_messages = UserMessage.objects.filter(user_id=self.request.user.pk)
        return user_messages

    def get_context_data(self, **kwargs):
        context = super(UserMessajeListView, self).get_context_data(**kwargs)

        context['page'] = self.page

        return context


class UserMessageDeleteView(LoginRequiredMixin, DeleteView):

    model = UserMessage
    template_name = 'core/user_messages/user_messages_confirm_delete.html'

    page = {
        'title': 'Message',
        'subtitle': 'detail'
    }

    def get_context_data(self, **kwargs):
        context = super(UserMessageDeleteView, self).get_context_data(**kwargs)
        context['page'] = self.page
        m = UserMessage.objects.get(pk=self.kwargs['pk'])
        m.unread = False
        m.save()
        return context

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'El mensaje ha sido eliminado satisfactoriamente')
        return reverse('core:user_messages_list')
