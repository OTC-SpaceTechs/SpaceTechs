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

from events.views import EventViewSet
from projects.views import ComponentViewSet, DocumentViewSet, ProjectViewSet, TipViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'tips', TipViewSet, basename='tip')
router.register(r'components', ComponentViewSet, basename='component')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('members/', include('membership.urls')),
    path('events/', include('events.urls')),
    path('api/', include(router.urls)),
]
