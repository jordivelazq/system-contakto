# -*- coding: utf-8 -*-

from app.agente.models import Labels
from django import forms
from django.forms import ModelForm

class LabelsForm(ModelForm):
  class Meta:
    model = Labels
    fields = ['color', 'name', 'agente']
    widgets = {
      'color': forms.HiddenInput(),
      'agente': forms.HiddenInput()
    }

  def __init__(self, *args, **kwargs):
    super(LabelsForm, self).__init__(*args, **kwargs)
    self.fields['name'].required = False

    for field_name, field in self.fields.items():
      field.widget.attrs['class'] = 'form-control'
