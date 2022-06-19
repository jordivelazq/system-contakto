from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from django.contrib.auth.models import User
from .serializers import UserSerializer


class UserTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'core/users_list.html'

    def get_context_data(self, **kwargs):
        context = super(UserTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
