# -*- coding: utf-8 -*-

import json

from django.shortcuts import HttpResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User

from app.investigacion.models import Investigacion
from app.compania.models import Contacto
from app.entrevista.controllerpersona import ControllerPersona

""" ----------------- EMPRESA -----------------"""


def empresa_get_contactos(request, empresa_id):
    data = serializers.serialize(
        "json",
        Contacto.objects.filter(compania_id=empresa_id, status=True).order_by("nombre"),
    )
    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_investigacion(request):
    if request.method != "POST":
        return JsonResponse({"status": "empty"})

    investigacion_id = 304
    user_id = 2

    investigacion = Investigacion.objects.get(id=investigacion_id)
    user = User.objects.get(id=user_id)
    data = {"candidato": json.loads(request.body.decode("utf8").replace("'", '"'))}
    candidato = ControllerPersona()
    candidato.saveAllData(investigacion, data, None, user)

    return JsonResponse({"status": "success"})
