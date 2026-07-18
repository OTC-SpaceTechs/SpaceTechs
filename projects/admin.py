from django.contrib import admin

from .models import Component, Document, Project, Tip


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0


class TipInline(admin.TabularInline):
    model = Tip
    extra = 0


class ComponentInline(admin.TabularInline):
    model = Component
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'start_date']
    list_filter = ['status']
    search_fields = ['name', 'description']
    inlines = [DocumentInline, ComponentInline, TipInline]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'doc_type', 'created_at']
    list_filter = ['doc_type']
    search_fields = ['title', 'content']


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['question', 'project', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['question', 'short_answer', 'content']


@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'quantity', 'cost', 'supplier']
    search_fields = ['name', 'supplier', 'notes']
