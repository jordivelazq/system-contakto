from django.http import HttpResponse
from oauth2_provider.models import AccessToken
from oauth2_provider.views import TokenView
import json

from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from app.investigacion.models import Investigacion
from app.persona.models import Persona


class AutenticateTokenView(TokenView):
    '''
     Login mobile app
    '''

    def post(self, request, *args, **kwargs):
        response = super(AutenticateTokenView, self).post(self.request, *args, **kwargs)
        try:
            token = json.loads(response.content.decode('utf-8')).get('access_token')
            if token:
                data = {
                    'key': json.loads(response.content.decode('utf-8')),
                }
                data = json.dumps(data)
            else:
                return HttpResponse([{"message": 'El usuario proporcionado no se encuentra en nuestros registros, verifique su información'}], status=response.status_code,
                                    content_type='application/json')
        except Exception as e:
            return HttpResponse([{"message": "Ha ocurrido un error, verifique su información", "error": e}], status=response.status_code, content_type='application/json')
        return HttpResponse(data, status=response.status_code, )