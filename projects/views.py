from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from rest_framework import viewsets

from core.generic_views import ExtraContextMixin
from core.permissions import IsOfficer, OfficerRequiredMixin, is_officer

from .forms import DocumentForm, ProjectForm, TipForm
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


class ProjectCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portal/object_form.html'
    title = 'Add Project'
    cancel_url = reverse_lazy('projects:project-list')

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', args=[self.object.pk])


class ProjectUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'portal/object_form.html'
    title = 'Edit Project'

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', args=[self.object.pk])


class ProjectDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = Project
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('projects:project-list')


class ProjectChildCreateMixin(OfficerRequiredMixin, ExtraContextMixin):
    """Shared plumbing for creating a Document/Tip nested under a Project."""

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=kwargs['project_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', args=[self.project.pk])

    def get_cancel_url(self):
        return reverse_lazy('projects:project-detail', args=[self.project.pk])


class ProjectChildEditMixin(OfficerRequiredMixin, ExtraContextMixin):
    """Shared plumbing for updating/deleting a Document/Tip. Both success and cancel go back to the parent project."""

    def get_success_url(self):
        return reverse_lazy('projects:project-detail', args=[self.object.project_id])

    def get_cancel_url(self):
        return reverse_lazy('projects:project-detail', args=[self.object.project_id])


class DocumentCreateView(ProjectChildCreateMixin, CreateView):
    model = Document
    form_class = DocumentForm
    template_name = 'portal/object_form.html'
    title = 'Add Document'


class DocumentUpdateView(ProjectChildEditMixin, UpdateView):
    model = Document
    form_class = DocumentForm
    template_name = 'portal/object_form.html'
    title = 'Edit Document'


class DocumentDeleteView(ProjectChildEditMixin, DeleteView):
    model = Document
    template_name = 'portal/object_confirm_delete.html'


class TipCreateView(ProjectChildCreateMixin, CreateView):
    model = Tip
    form_class = TipForm
    template_name = 'portal/object_form.html'
    title = 'Add Tip'


class TipUpdateView(ProjectChildEditMixin, UpdateView):
    model = Tip
    form_class = TipForm
    template_name = 'portal/object_form.html'
    title = 'Edit Tip'


class TipDeleteView(ProjectChildEditMixin, DeleteView):
    model = Tip
    template_name = 'portal/object_confirm_delete.html'


class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    """Public project showcase. Overview only, no nested documents or tips."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """Full project documentation. Officers only."""
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsOfficer]


class TipViewSet(viewsets.ReadOnlyModelViewSet):
    """Tips. Officers only."""
    queryset = Tip.objects.all()
    serializer_class = TipSerializer
    permission_classes = [IsOfficer]
