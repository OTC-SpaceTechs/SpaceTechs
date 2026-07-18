from django.shortcuts import get_object_or_404, render

from core.permissions import officer_required

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
