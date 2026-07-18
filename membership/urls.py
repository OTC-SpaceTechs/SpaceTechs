from django.urls import path

from . import views

app_name = 'membership'

urlpatterns = [
    path('', views.member_list, name='member-list'),
    path('new/', views.MemberCreateView.as_view(), name='member-create'),
    path('<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('<int:pk>/edit/', views.MemberUpdateView.as_view(), name='member-update'),
    path('<int:pk>/delete/', views.MemberDeleteView.as_view(), name='member-delete'),
    path('<int:member_pk>/officer-history/new/', views.OfficerHistoryCreateView.as_view(), name='officer-history-create'),
    path('officer-history/<int:pk>/edit/', views.OfficerHistoryUpdateView.as_view(), name='officer-history-update'),
    path('officer-history/<int:pk>/delete/', views.OfficerHistoryDeleteView.as_view(), name='officer-history-delete'),
]
