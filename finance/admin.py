from django.contrib import admin

from .models import PurchaseRequest


@admin.register(PurchaseRequest)
class PurchaseRequestAdmin(admin.ModelAdmin):
    list_display = ['requested_by', 'amount', 'project', 'status', 'approved_by', 'created_at']
    list_filter = ['status']
    search_fields = ['purpose', 'requested_by__user__username']
