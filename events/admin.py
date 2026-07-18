from django.contrib import admin

from .models import Article, ArticleImage, Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'event_type', 'location']
    list_filter = ['event_type']
    search_fields = ['title', 'description', 'location']
    date_hierarchy = 'date'


class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'published_at']
    search_fields = ['title', 'summary', 'body']
    date_hierarchy = 'published_at'
    inlines = [ArticleImageInline]
