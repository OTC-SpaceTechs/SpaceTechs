from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.equipment_list, name='equipment-list'),
    path('<int:pk>/', views.equipment_detail, name='equipment-detail'),
]
