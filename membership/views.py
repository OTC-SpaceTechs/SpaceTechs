from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from core.generic_views import ExtraContextMixin
from core.permissions import OfficerRequiredMixin, officer_required

from .forms import MemberForm, OfficerHistoryForm
from .models import Member, OfficerHistory


@officer_required
def member_list(request):
    query = request.GET.get('q', '').strip()
    members = Member.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    if query:
        members = members.filter(
            Q(user__first_name__icontains=query)
            | Q(user__last_name__icontains=query)
            | Q(user__username__icontains=query)
            | Q(major__icontains=query)
        )
    return render(request, 'membership/member_list.html', {'members': members, 'query': query})


class MemberDetailView(OfficerRequiredMixin, DetailView):
    model = Member
    template_name = 'membership/member_detail.html'
    context_object_name = 'member'

    def get_queryset(self):
        return Member.objects.select_related('user').prefetch_related('officerhistory_set__role')


class MemberCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = Member
    form_class = MemberForm
    template_name = 'portal/object_form.html'
    title = 'Add Member'
    success_url = reverse_lazy('portal:membership:member-list')


class MemberUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = Member
    form_class = MemberForm
    template_name = 'portal/object_form.html'
    title = 'Edit Member'

    def get_success_url(self):
        return reverse_lazy('portal:membership:member-detail', args=[self.object.pk])


class MemberDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = Member
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('portal:membership:member-list')


class OfficerHistoryCreateView(OfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = OfficerHistory
    form_class = OfficerHistoryForm
    template_name = 'portal/object_form.html'
    title = 'Add Officer History Entry'

    def dispatch(self, request, *args, **kwargs):
        self.member = get_object_or_404(Member, pk=kwargs['member_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.member = self.member
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('portal:membership:member-detail', args=[self.member.pk])


class OfficerHistoryUpdateView(OfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = OfficerHistory
    form_class = OfficerHistoryForm
    template_name = 'portal/object_form.html'
    title = 'Edit Officer History Entry'

    def get_success_url(self):
        return reverse_lazy('portal:membership:member-detail', args=[self.object.member.pk])


class OfficerHistoryDeleteView(OfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = OfficerHistory
    template_name = 'portal/object_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('portal:membership:member-detail', args=[self.object.member.pk])
