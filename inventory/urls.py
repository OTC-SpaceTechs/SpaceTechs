from django.urls import path

from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.equipment_list, name='equipment-list'),
    path('new/', views.EquipmentCreateView.as_view(), name='equipment-create'),
    path('<int:pk>/', views.equipment_detail, name='equipment-detail'),
    path('<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name='equipment-update'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment-delete'),
]
