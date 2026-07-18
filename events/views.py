import calendar

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, UpdateView
from rest_framework import viewsets

from core.generic_views import ExtraContextMixin
from core.permissions import OfficerRequiredMixin, officer_required
from membership.models import Member

from .forms import ArticleForm, ArticleImageForm, EventForm
from .models import Article, ArticleImage, Event
from .serializers import ArticleSerializer, EventSerializer

MONTH_NAMES = [
    '', 'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December',
]


def _build_month_grid(year, month, events):
    events_by_day = {}
    for event in events:
        day = timezone.localtime(event.date).date()
        events_by_day.setdefault(day, []).append(event)

    today = timezone.localdate()
    cal = calendar.Calendar(firstweekday=6)  # weeks start on Sunday
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        weeks.append([
            {
                'date': day,
                'in_month': day.month == month,
                'is_today': day == today,
                'events': events_by_day.get(day, []),
            }
            for day in week
        ])
    return weeks


def events_home(request):
    today = timezone.localdate()
    try:
        year = int(request.GET.get('year', today.year))
        month = int(request.GET.get('month', today.month))
        if not 1 <= month <= 12:
            raise ValueError
    except (TypeError, ValueError):
        year, month = today.year, today.month

    month_events = Event.objects.filter(date__year=year, date__month=month)
    weeks = _build_month_grid(year, month, month_events)

    prev_year, prev_month = (year - 1, 12) if month == 1 else (year, month - 1)
    next_year, next_month = (year + 1, 1) if month == 12 else (year, month + 1)

    articles = Article.objects.select_related('author__user')[:6]

    context = {
        'weeks': weeks,
        'month_label': f"{MONTH_NAMES[month]} {year}",
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today_year': today.year,
        'today_month': today.month,
        'articles': articles,
    }
    return render(request, 'events/events_home.html', context)


def event_table(request):
    query = request.GET.get('q', '').strip()
    events = Event.objects.all()
    if query:
        events = events.filter(Q(title__icontains=query) | Q(location__icontains=query) | Q(description__icontains=query))
    return render(request, 'events/event_table.html', {'events': events, 'query': query})


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


def article_list(request):
    query = request.GET.get('q', '').strip()
    articles = Article.objects.select_related('author__user')
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(body__icontains=query))
    paginator = Paginator(articles, 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'events/article_list.html', {'page_obj': page_obj, 'query': query})


def article_detail(request, pk):
    article = get_object_or_404(Article.objects.select_related('author__user'), pk=pk)
    return render(request, 'events/article_detail.html', {'article': article})


class ArticleCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'events/article_form.html'
    title = 'Write Article'
    cancel_url = reverse_lazy('events:event-list')

    def form_valid(self, form):
        form.instance.author = Member.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('events:article-detail', args=[self.object.pk])


class ArticleUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'events/article_form.html'
    title = 'Edit Article'

    def get_success_url(self):
        return reverse_lazy('events:article-detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        context['photo_form'] = ArticleImageForm()
        return context


class ArticleDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = Article
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('events:article-list')


@officer_required
def article_photo_upload(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method != 'POST':
        return redirect('events:article-update', pk=article.pk)

    photo_form = ArticleImageForm(request.POST, request.FILES)
    if photo_form.is_valid():
        photo = photo_form.save(commit=False)
        photo.article = article
        photo.save()
        return redirect('events:article-update', pk=article.pk)

    # Invalid upload: re-render the edit page so the error shows next to the upload form.
    context = {
        'form': ArticleForm(instance=article),
        'photo_form': photo_form,
        'photos': article.photos.all(),
        'title': 'Edit Article',
        'cancel_url': reverse('events:article-list'),
        'object': article,
    }
    return render(request, 'events/article_form.html', context)


class ArticleImageDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = ArticleImage
    template_name = 'portal/object_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('events:article-update', args=[self.object.article_id])

    def get_cancel_url(self):
        return reverse_lazy('events:article-update', args=[self.object.article_id])


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
