# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from app.clientes.models import ClienteUser
from app.compania.models import Compania
from ..forms.clientes_users_form import ClienteUserForm, ClienteUserEditForm, ClienteUserPasswdForm


class ClienteUserCreateView(GroupRequiredMixin, CreateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = ClienteUser
    form_class = ClienteUserForm
    success_url = reverse_lazy('clientes:clientes_list')
    template_name = 'clientes/clientes_users/clientes_user_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteUserCreateView, self).get_context_data(**kwargs)

        context['form'].fields['compania'].queryset = Compania.objects.filter(es_cliente=True)

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password1'])
        self.object.username = form.cleaned_data['username']
        self.object.email = form.cleaned_data['username']
        self.object.save()
        # self.object.groups.add(Group.objects.get(name='Usuarios'))
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'The user was created successfully')

        super(ClienteUserCreateView, self).form_valid(form)

        return redirect(self.success_url)


class ClienteUserDetailView(GroupRequiredMixin, DetailView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = ClienteUser
    template_name = 'clientes/clientes_users/clientes_user_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteUserDetailView, self).get_context_data(**kwargs)
        context['form'].fields['compania'].queryset = Compania.objects.filter(es_cliente=True)
        return context


class ClienteUserUpdateView(GroupRequiredMixin, UpdateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = ClienteUser
    form_class = ClienteUserEditForm
    success_url = reverse_lazy('clientes:clientes_list')
    template_name = 'clientes/clientes_users/clientes_user_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteUserUpdateView, self).get_context_data(**kwargs)

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(self.request, messages.SUCCESS, 'User data has been updated')

        super(ClienteUserUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class ClienteUserUpdatePasswdView(GroupRequiredMixin, UpdateView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = ClienteUser
    form_class = ClienteUserPasswdForm
    success_url = reverse_lazy('clientes:clientes_list')
    template_name = 'clientes/clientes_users/clientes_user_form.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteUserUpdatePasswdView, self).get_context_data(**kwargs)
        context['page'] = {
            'title': _('User'),
            'subtitle': _('password change'),
        }

        return context

    def form_valid(self, form):

        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data['password1'])
        self.object.save()

        messages.add_message(self.request,
                             messages.SUCCESS, 'The password has been updated')

        super(ClienteUserUpdatePasswdView, self).form_valid(form)

        return redirect(self.success_url)


class ClienteUserDelete(GroupRequiredMixin, DeleteView):

    # required
    group_required = u"SuperAdmin"
    raise_exception = True

    model = ClienteUser

    template_name = 'clientes/clientes_users/clientes_user_confirm_delete.html'

    page = {
        'title': _('User'),
        'subtitle': _('delete')
    }

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS,  'User has been successfully removed')
        return reverse('clientes:clientes_list')

    def get_context_data(self, **kwargs):
        context = super(ClienteUserDelete, self).get_context_data(**kwargs)
        context['page'] = self.page

        return context
