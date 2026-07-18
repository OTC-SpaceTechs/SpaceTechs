"""
URL configuration for spacetechs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import home, portal_home, portal_search

from events.views import EventViewSet
from projects.views import DocumentViewSet, ProjectViewSet, TipViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'tips', TipViewSet, basename='tip')

# Officer-only portal: member roster, inventory, and cross-project search.
# Finance stays admin-only (see finance/admin.py) rather than getting its own portal page.
portal_patterns = [
    path('', portal_home, name='home'),
    path('search/', portal_search, name='search'),
    path('members/', include('membership.urls')),
    path('inventory/', include('inventory.urls')),
]

urlpatterns = [
    path('', home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('portal/', include((portal_patterns, 'portal'), namespace='portal')),
    path('events/', include('events.urls')),
    path('projects/', include('projects.urls')),
    path('api/', include(router.urls)),
]
