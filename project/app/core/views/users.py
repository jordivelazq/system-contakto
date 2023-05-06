# -*- coding: utf-8 -*-
from braces.views import GroupRequiredMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from ..forms.users_form import UserEditForm, UserForm, UserPasswdForm


class UserCreateView(GroupRequiredMixin, CreateView):
    '''Create a user'''
    # required
    group_required = "SuperAdmin"
    raise_exception = True

    model = User
    form_class = UserForm
    success_url = reverse_lazy("core:users_list")
    template_name = "core/users/user_form.html"

    page = {"title": _("User"), "subtitle": _("Add")}

    def get_context_data(self, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context["page"] = self.page

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data["password1"])
        self.object.username = form.cleaned_data["username"]
        self.object.email = form.cleaned_data["username"]
        self.object.save()
        # self.object.groups.add(Group.objects.get(name='Usuarios'))
        self.object.save()

        messages.add_message(
            self.request, messages.SUCCESS,
            _("The user was created successfully")
        )

        super(UserCreateView, self).form_valid(form)

        return redirect(self.success_url)


class UserDetailView(GroupRequiredMixin, DetailView):
    '''Detail of a user'''
    # required
    group_required = "SuperAdmin"
    raise_exception = True

    model = User
    template_name = "core/users/user_detail.html"

    page = {"title": _("User"), "subtitle": _("Detail")}

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context["page"] = self.page
        return context


class UserUpdateView(GroupRequiredMixin, UpdateView):
    '''Update a user'''
    # required
    group_required = "SuperAdmin"
    raise_exception = True

    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("core:users_list")
    template_name = "core/users/user_form.html"

    page = {"title": _("User"), "subtitle": _("Update")}

    def get_context_data(self, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)

        context["page"] = self.page

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()

        messages.add_message(
            self.request, messages.SUCCESS, _("User data has been updated")
        )

        super(UserUpdateView, self).form_valid(form)

        return redirect(self.success_url)


class UserUpdatePasswdView(GroupRequiredMixin, UpdateView):
    '''Update a user password'''
    # required
    group_required = "SuperAdmin"
    raise_exception = True

    model = User
    form_class = UserPasswdForm
    success_url = reverse_lazy("core:users_list")
    template_name = "core/users/user_form.html"

    def get_context_data(self, **kwargs):
        context = super(UserUpdatePasswdView, self).get_context_data(**kwargs)
        context["page"] = {
            "title": _("User"),
            "subtitle": _("password change"),
        }

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_password(form.cleaned_data["password1"])
        self.object.save()

        messages.add_message(
            self.request, messages.SUCCESS, _("The password has been updated")
        )

        super(UserUpdatePasswdView, self).form_valid(form)

        return redirect(self.success_url)


class UserDelete(GroupRequiredMixin, DeleteView):
    '''Delete a user'''

    # required
    group_required = "SuperAdmin"
    raise_exception = True

    model = User

    template_name = "core/users/user_confirm_delete.html"

    page = {"title": _("User"), "subtitle": _("delete")}

    # send the user back to their own page after a successful update
    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            _("User has been successfully removed")
        )
        return reverse("core:users_list")

    def get_context_data(self, **kwargs):
        context = super(UserDelete, self).get_context_data(**kwargs)
        context["page"] = self.page

        return context
