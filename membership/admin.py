from django.contrib import admin
from .models import Member, OfficerHistory


class OfficerHistoryInline(admin.TabularInline):
    model = OfficerHistory
    extra = 0


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'join_date', 'active_status', 'major']
    list_filter = ['active_status']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'major']
    inlines = [OfficerHistoryInline]


@admin.register(OfficerHistory)
class OfficerHistoryAdmin(admin.ModelAdmin):
    list_display = ['member', 'role', 'start_date', 'end_date']
    list_filter = ['role']
