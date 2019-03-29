"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .forms import CandidatoAltaForm

class CandidatoAltaFormTest(TestCase):
  def test_invalid_form(self):
    data = {}
    form = CandidatoAltaForm(data)

    self.assertFalse(form.is_valid())

  def test_valid_form(self):
    data = {
      'nombre': 'nombre persona',
    }
    form = CandidatoAltaForm(data)

    self.assertTrue(form.is_valid())

  def test_invalid_form_nss(self):
    data = {
      'nombre': 'nombre persona',
      'nss': 'nss'
    }
    form = CandidatoAltaForm(data)

    self.assertFalse(form.is_valid())

  def test_valid_form_rfc(self):
    data = {
      'nombre': 'nombre persona',
      'nss': '12345678901'
    }
    form = CandidatoAltaForm(data)

    self.assertTrue(form.is_valid())

  def test_invalid_form_curp(self):
    data = {
      'nombre': 'nombre persona',
      'curp': 'curp'
    }
    form = CandidatoAltaForm(data)

    self.assertFalse(form.is_valid())

  def test_valid_form_curp(self):
    data = {
      'nombre': 'nombre persona',
      'curp': '123456789012345678'
    }
    form = CandidatoAltaForm(data)

    self.assertTrue(form.is_valid())
