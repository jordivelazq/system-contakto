"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .forms import CompaniaForm

class CompaniaFormTest(TestCase):
  def test_invalid_form(self):
    data = {}
    form = CompaniaForm(data)

    self.assertFalse(form.is_valid())

  def test_valid_form(self):
    data = {
      'nombre': 'nombre empresa',
    }
    form = CompaniaForm(data)

    self.assertTrue(form.is_valid())

  def test_invalid_form_rfc(self):
    data = {
      'nombre': 'nombre empresa',
      'rfc': 'rfc'
    }
    form = CompaniaForm(data)

    self.assertFalse(form.is_valid())

  def test_valid_form_rfc(self):
    data = {
      'nombre': 'nombre empresa',
      'rfc': '1234567890123'
    }
    form = CompaniaForm(data)

    self.assertTrue(form.is_valid())
