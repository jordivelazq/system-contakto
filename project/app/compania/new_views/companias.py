from django.urls import reverse_lazy
from ..models import Compania, Sucursales, Contacto, DireccionFiscal
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from app.clientes.models import ClienteUser


class CompaniaDetailView(DetailView):
    model = Compania
    template_name = 'companias/compania/compania_detail.html'
    context_object_name = 'compania'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del cliente'
        context['clientes'] = ClienteUser.objects.filter(compania=self.object)
        return context


class CompaniaCreateView(CreateView):
    model = Compania
    template_name = 'companias/compania/compania_form.html'
    fields = ('__all__')
    compania_id = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear cliente'
        context['form'].fields['coordinador_ejecutivos'].queryset = User.objects.filter(groups__name='Coordinador de Ejecutivos')
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.compania_id = self.object.id
        return super(CompaniaCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El cliente ha sido agregado correctamente')
        return reverse('companias_detail', kwargs={"pk": self.compania_id})


class CompaniaUpdateView(UpdateView):
    model = Compania
    template_name = 'companias/compania/compania_form.html'
    fields = ('__all__')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar cliente'
        context['compania_id'] = self.kwargs['pk']
        context['form'].fields['coordinador_ejecutivos'].queryset = User.objects.filter(groups__name='Coordinador de Ejecutivos')
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El cliente ha sido actualizado correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['pk']})


class CompaniaDeleteView(DeleteView):
    model = Compania
    context_object_name = 'compania'
    template_name = 'companias/compania/compania_delete.html'
    success_url = reverse_lazy('companias_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar cliente'
        return context


class CompaniaSucursalCreateView(CreateView):

    model = Sucursales
    template_name = 'companias/sucursales/sucursal_form.html'
    fields = ['nombre', 'ciudad', 'telefono', 'email', 'estado', 'municipio',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear sucursal'
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
    fields = ['nombre', 'ciudad', 'telefono', 'email', 'estado', 'municipio',]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar sucursal'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'La sucursal ha sido actualizada correctamente')
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
                             'La sucursal ha sido eliminada correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})



class DireccionFiscalCreateView(CreateView):

    model = DireccionFiscal
    template_name = 'companias/direcciones_fiscales/direccion_fiscal_form.html'
    fields = ['regimen_fiscal', 'rfc', 'nombre', 'direccion', 'codigo_postal', 'estado', 'municipio', 'activo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear datos fiscales'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.compania_id = self.kwargs['compania_id']
        self.object.save()
        return super(DireccionFiscalCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Los datos fiscales han sido agregados correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class DireccionFiscalUpdateView(UpdateView):

    model = DireccionFiscal
    template_name = 'companias/direcciones_fiscales/direccion_fiscal_form.html'
    fields = ['regimen_fiscal', 'rfc', 'nombre', 'direccion', 'codigo_postal', 'estado', 'municipio', 'activo']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar datos fiscales'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Los datos fiscales han sido actualizados correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class DireccionFiscalDeleteView(DeleteView):
    model = DireccionFiscal
    context_object_name = 'direccion_fiscal'
    template_name = 'companias/direcciones_fiscales/direccion_fiscal_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar datos fiscales'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'Los datos fiscales han sido eliminados correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoCreateView(CreateView):

    model = Contacto
    template_name = 'companias/contactos/contacto_form.html'
    fields = ['nombre', 'puesto', 'email', 'email_alt', 'telefono', 'telefono_celular',
              'telefono_otro', 'costo_inv_laboral', 'costo_inv_completa', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear contacto'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def form_valid(self, form, **kwargs):
        self.object = form.save(commit=False)
        self.object.compania_id = self.kwargs['compania_id']
        self.object.save()
        return super(CompaniaContactoCreateView, self).form_valid(form)

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El contacto ha sido agregado correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoUpdateView(UpdateView):

    model = Contacto
    template_name = 'companias/contactos/contacto_form.html'
    fields = ['nombre', 'puesto', 'email', 'email_alt', 'telefono', 'telefono_celular',
              'telefono_otro', 'costo_inv_laboral', 'costo_inv_completa', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar contacto'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El contacto ha sido actualizado correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})


class CompaniaContactoDeleteView(DeleteView):

    model = Contacto
    context_object_name = 'contacto'
    template_name = 'companias/contactos/contacto_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar contacto'
        context['compania_id'] = self.kwargs['compania_id']
        return context

    def get_success_url(self, **kwargs):
        messages.add_message(self.request, messages.SUCCESS,
                             'El contacto ha sido eliminado correctamente')
        return reverse('companias_detail', kwargs={"pk": self.kwargs['compania_id']})
