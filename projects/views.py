from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets

from core.permissions import IsOfficer, is_officer

from .models import Document, Project, Tip
from .serializers import DocumentSerializer, ProjectSerializer, TipSerializer


def project_list(request):
    projects = Project.objects.all().order_by('-start_date')
    return render(request, 'projects/project_list.html', {'projects': projects})


def project_detail(request, pk):
    officer = is_officer(request.user)
    if officer:
        project = get_object_or_404(
            Project.objects.prefetch_related('documents', 'tips', 'equipment_checked_out'),
            pk=pk,
        )
    else:
        project = get_object_or_404(Project, pk=pk)
    return render(request, 'projects/project_detail.html', {'project': project})


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Public project showcase — overview only, no nested documents/tips."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """Full project documentation — officers only."""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOfficer]


class TipViewSet(viewsets.ReadOnlyModelViewSet):
    """Lessons learned — officers only."""
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsOfficer]
