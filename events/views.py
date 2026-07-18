from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from rest_framework import viewsets
from django.views.generic import CreateView, DeleteView, UpdateView

from core.generic_views import ExtraContextMixin
from core.permissions import OfficerRequiredMixin

from .forms import EventForm
from .models import Event
from .serializers import EventSerializer


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})


class EventCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'portal/object_form.html'
    title = 'Add Event'
    success_url = reverse_lazy('events:event-list')


class EventUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'portal/object_form.html'
    title = 'Edit Event'

    def get_success_url(self):
        return reverse_lazy('events:event-detail', args=[self.object.pk])


class EventDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = Event
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('events:event-list')


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
