from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from rest_framework import mixins, viewsets

from .models import ClienteUser
from .serializers import ClienteUserSerializer


class ClienteTemplateView(LoginRequiredMixin, TemplateView):

    template_name = 'clientes/clientes_users/clientes_users_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteTemplateView, self).get_context_data(**kwargs)
        context['title'] = 'Clientes'

        return context


class ClienteUserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = ClienteUser.objects.all()
    serializer_class = ClienteUserSerializer
