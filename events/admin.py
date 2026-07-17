from django.contrib import admin

from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'location']
    list_filter = ['event_type']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'
