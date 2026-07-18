from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from finance.models import PurchaseRequest
from inventory.models import Equipment
from membership.models import Member
from projects.models import Document, Project, Tip

from .permissions import officer_required


def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    active_projects = Project.objects.filter(status=Project.Status.ACTIVE).order_by('-start_date')[:6]
    context = {
        'upcoming_events': upcoming_events,
        'active_projects': active_projects,
    }
    return render(request, 'core/home.html', context)


@officer_required
def portal_home(request):
    context = {
        'member_count': Member.objects.filter(active_status=True).count(),
        'equipment_count': Equipment.objects.count(),
        'pending_purchase_requests': PurchaseRequest.objects.filter(status='PENDING').count(),
        'project_count': Project.objects.count(),
        'upcoming_event_count': Event.objects.filter(date__gte=timezone.now()).count(),
    }
    return render(request, 'core/portal_home.html', context)


@officer_required
def portal_search(request):
    query = request.GET.get('q', '').strip()
    documents = []
    tips = []

    if query:
        search_query = SearchQuery(query)

        documents = (
            Document.objects
            .annotate(rank=SearchRank(SearchVector('title', 'content'), search_query))
            .filter(rank__gt=0)
            .select_related('project')
            .order_by('-rank')
        )
        tips = (
            Tip.objects
            .annotate(rank=SearchRank(SearchVector('question', 'short_answer', 'content', 'category'), search_query))
            .filter(rank__gt=0)
            .select_related('project')
            .order_by('-rank')
        )

    context = {
        'query': query,
        'documents': documents,
        'tips': tips,
    }
    return render(request, 'core/portal_search.html', context)
