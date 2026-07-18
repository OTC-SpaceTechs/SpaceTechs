from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone

from events.models import Article, Event
from finance.models import PurchaseRequest
from inventory.models import Equipment
from membership.models import Member
from projects.models import Document, Project, Tip

from .permissions import officer_required


def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:5]
    active_projects = Project.objects.filter(status=Project.Status.ACTIVE).order_by('-start_date')[:6]
    recent_articles = Article.objects.select_related('author__user')[:3]
    context = {
        'upcoming_events': upcoming_events,
        'active_projects': active_projects,
        'recent_articles': recent_articles,
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

        # Filenames don't tokenize well through Postgres full-text search (underscores,
        # extensions, etc.), so match them as a plain substring alongside the ranked
        # title/content search rather than folding them into the text vector.
        #
        # Filtering on rank__gt=0 (rather than the `search=search_query` match below)
        # is unreliable: ts_rank can return a tiny float epsilon instead of an exact 0
        # for non-matches, which silently matched every row regardless of query.
        doc_vector = SearchVector('title', 'content')
        documents = (
            Document.objects
            .annotate(search=doc_vector, rank=SearchRank(doc_vector, search_query))
            .filter(Q(search=search_query) | Q(file__icontains=query) | Q(image__icontains=query))
            .select_related('project')
            .order_by('-rank')
        )

        tip_vector = SearchVector('question', 'short_answer', 'content', 'category')
        tips = (
            Tip.objects
            .annotate(search=tip_vector, rank=SearchRank(tip_vector, search_query))
            .filter(Q(search=search_query) | Q(image__icontains=query))
            .select_related('project')
            .order_by('-rank')
        )

    context = {
        'query': query,
        'documents': documents,
        'tips': tips,
    }
    return render(request, 'core/portal_search.html', context)
