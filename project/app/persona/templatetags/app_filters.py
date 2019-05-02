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

@register.filter(name='print_page_number')
def print_page_number(number, base):
  return base + number

@register.filter(name='verbose_name')
def verbose_name(instance, field_name):
  return instance._meta.get_field(field_name).verbose_name.title()

@register.filter(name='localize_month')
def localize_month(instance):
    months = [ ('JAN', 'ENE'), ('APR', 'ABR'), ('AUG', 'AGO'), ('DEC', 'DIC')]
    for en, es in months:
      instance = instance.upper().replace(en, es)
    return instance
