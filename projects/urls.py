from django.urls import path

from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_list, name='project-list'),
    path('new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/', views.project_detail, name='project-detail'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:project_pk>/documents/new/', views.DocumentCreateView.as_view(), name='document-create'),
    path('documents/<int:pk>/edit/', views.DocumentUpdateView.as_view(), name='document-update'),
    path('documents/<int:pk>/delete/', views.DocumentDeleteView.as_view(), name='document-delete'),
    path('<int:project_pk>/tips/new/', views.TipCreateView.as_view(), name='tip-create'),
    path('tips/<int:pk>/edit/', views.TipUpdateView.as_view(), name='tip-update'),
    path('tips/<int:pk>/delete/', views.TipDeleteView.as_view(), name='tip-delete'),
]
