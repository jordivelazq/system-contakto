from django.urls import reverse_lazy
from ..models import Compania, Sucursales, Contacto
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib import messages
from django.urls import reverse, reverse_lazy


class CompaniaDetailView(DetailView):
    model = Compania
    template_name = 'companias/compania/compania_detail.html'
    context_object_name = 'compania'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Compañia'
        return context


class CompaniaCreateView(CreateView):
    model = Compania
    template_name = 'companias/compania/compania_form.html'
    fields = ('__all__')
    compania_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Compañia'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.compania_id = self.object.id
        return super(CompaniaCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido agregada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.compania_id})


class CompaniaUpdateView(UpdateView):
    model = Compania
    template_name = 'companias/compania/compania_form.html'
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Compañia'
        context['compania_id'] = self.kwargs['pk']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido actualizada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['pk']})


class CompaniaDeleteView(DeleteView):
    model = Compania
    context_object_name = 'compania'
    template_name = 'companias/compania/compania_delete.html'
    success_url = reverse_lazy('companias_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Compañia'
        return context


class CompaniaSucursalCreateView(CreateView):

    model = Sucursales
    template_name = 'companias/sucursales/sucursal_form.html'
    fields = ['nombre', 'ciudad', 'telefono', 'email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Compañia'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.compania_id = self.kwargs['compania_id']
        self.object.save()
        return super(CompaniaSucursalCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La sucursal ha sido agregada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaSucursalUpdateView(UpdateView):

    model = Sucursales
    template_name = 'companias/sucursales/sucursal_form.html'
    fields = ['nombre', 'ciudad', 'telefono', 'email']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Compañia'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido actualizada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaSucursalDeleteView(DeleteView):
    model = Sucursales
    context_object_name = 'sucursal'
    template_name = 'companias/sucursales/sucursal_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Sucursal'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido eliminada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoCreateView(CreateView):

    model = Contacto
    template_name = 'companias/contactos/contacto_form.html'
    fields = ['nombre', 'puesto', 'email', 'email_alt', 'telefono', 'telefono_celular',
              'telefono_otro', 'costo_inv_laboral', 'costo_inv_completa', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Compañia'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.compania_id = self.kwargs['compania_id']
        self.object.save()
        return super(CompaniaContactoCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La sucursal ha sido agregada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoUpdateView(UpdateView):

    model = Contacto
    template_name = 'companias/contactos/contacto_form.html'
    fields = ['nombre', 'puesto', 'email', 'email_alt', 'telefono', 'telefono_celular',
              'telefono_otro', 'costo_inv_laboral', 'costo_inv_completa', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar contacto de emprea'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido actualizada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoDeleteView(DeleteView):

    model = Contacto
    context_object_name = 'contacto'
    template_name = 'companias/contactos/contacto_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar contacto de empresa'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El empresa ha sido eliminada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})
