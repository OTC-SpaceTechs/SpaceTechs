from rest_framework import viewsets

from .models import Component, Document, Project, Tip
from .serializers import ComponentSerializer, DocumentSerializer, ProjectSerializer, TipSerializer


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class TipViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tip.objects.all()
    serializer_class = TipSerializer


class ComponentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer
