from django.contrib import admin
from .models import Equipment

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'cost', 'supplier', 'custodian', 'checked_out_to_project', 'approved_by']
    search_fields = ['name', 'supplier', 'notes']