from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic_views import ExtraContextMixin
from core.permissions import OfficerRequiredMixin, officer_required

from .forms import EquipmentForm
from .models import Equipment


@officer_required
def equipment_list(request):
    equipment = Equipment.objects.select_related('custodian__user', 'checked_out_to_project').order_by('name')
    return render(request, 'inventory/equipment_list.html', {'equipment': equipment})


@officer_required
def equipment_detail(request, pk):
    item = get_object_or_404(
        Equipment.objects.select_related('custodian__user', 'checked_out_to_project', 'approved_by__user'),
        pk=pk,
    )
    return render(request, 'inventory/equipment_detail.html', {'item': item})


class EquipmentCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'portal/object_form.html'
    title = 'Add Equipment'
    success_url = reverse_lazy('portal:inventory:equipment-list')


class EquipmentUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = Equipment
    form_class = EquipmentForm
    template_name = 'portal/object_form.html'
    title = 'Edit Equipment'

    def get_success_url(self):
        return reverse_lazy('portal:inventory:equipment-detail', args=[self.object.pk])


class EquipmentDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = Equipment
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('portal:inventory:equipment-list')
