from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('new/', views.EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/', views.event_detail, name='event-detail'),
    path('<int:pk>/edit/', views.EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/delete/', views.EventDeleteView.as_view(), name='event-delete'),
]
