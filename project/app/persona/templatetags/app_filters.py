from django import template

register = template.Library()

from app.persona.models import Evaluacion

@register.filter(name='activo_opciones')
def activo_opciones(value):
  if value == 1:
    return "si"
  elif value == 2:
    return "no"
  return ""

@register.filter(name='activo_opciones_con_x')
def activo_opciones(value, flag):
  if value == flag:
    return "X"
  return ""

@register.filter(name='evaluacion_opciones')
def evaluacion_opciones(evaluacion, tipo):
  value = getattr(evaluacion, tipo)
  if value:
    return Evaluacion.EVALUACION_OPCIONES[int(value)-1][1][0]
  return ""

@register.filter(name='get_opinion')
def get_opinion(trayectoria, categoria):
  if trayectoria.evaluacion_set.count():
    evaluacion = trayectoria.evaluacion_set.all()[0]
    opinion = evaluacion.opinion_set.filter(categoria=categoria)
    if opinion.count():
      return opinion[0].opinion

  return ""

@register.filter(name='get_informante')
def get_informante(trayectoria, index):
  if trayectoria.evaluacion_set.count():
    evaluacion = trayectoria.evaluacion_set.all()[0]
    informantes = evaluacion.informante_set.all()
    if index < informantes.count():
      return informantes[index].nombre

  return ""

@register.filter(name='get_informante_puesto')
def get_informante_puesto(trayectoria, index):
  if trayectoria.evaluacion_set.count():
    evaluacion = trayectoria.evaluacion_set.all()[0]
    informantes = evaluacion.informante_set.all()
    if index < informantes.count():
      return informantes[index].puesto

  return ""

@register.filter(name='print_page_number')
def print_page_number(number, base):
  return base + number

@register.filter(name='verbose_name')
def verbose_name(instance, field_name):
  return instance._meta.get_field(field_name).verbose_name.title()
