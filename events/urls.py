from django.urls import path

from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event-list'),
    path('<int:pk>/', views.event_detail, name='event-detail'),
]
