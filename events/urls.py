from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.events_home, name='event-list'),
    path('list/', views.event_table, name='event-table'),
    path('new/', views.EventCreateView.as_view(), name='event-create'),
    path('articles/', views.article_list, name='article-list'),
    path('articles/new/', views.ArticleCreateView.as_view(), name='article-create'),
    path('articles/<int:pk>/', views.article_detail, name='article-detail'),
    path('articles/<int:pk>/edit/', views.ArticleUpdateView.as_view(), name='article-update'),
    path('articles/<int:pk>/delete/', views.ArticleDeleteView.as_view(), name='article-delete'),
    path('articles/<int:article_pk>/images/', views.article_photo_upload, name='article-images'),
    path('articles/images/<int:pk>/delete/', views.ArticleImageDeleteView.as_view(), name='article-image-delete'),
    path('<int:pk>/', views.event_detail, name='event-detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
]
