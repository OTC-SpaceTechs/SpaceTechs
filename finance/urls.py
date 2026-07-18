from django.urls import path

from . import views

app_name = 'finance'

urlpatterns = [
    path('', views.PurchaseRequestListView.as_view(), name='purchase-request-list'),
    path('new/', views.PurchaseRequestCreateView.as_view(), name='purchase-request-create'),
    path('<int:pk>/', views.PurchaseRequestDetailView.as_view(), name='purchase-request-detail'),
    path('<int:pk>/edit/', views.PurchaseRequestUpdateView.as_view(), name='purchase-request-update'),
    path('<int:pk>/delete/', views.PurchaseRequestDeleteView.as_view(), name='purchase-request-delete'),
]
