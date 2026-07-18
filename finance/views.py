from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.generic_views import ExtraContextMixin
from core.permissions import FinanceOfficerRequiredMixin
from membership.models import Member

from .forms import PurchaseRequestCreateForm, PurchaseRequestUpdateForm
from .models import PurchaseRequest


class PurchaseRequestListView(FinanceOfficerRequiredMixin, ListView):
    template_name = 'finance/purchaserequest_list.html'
    context_object_name = 'purchase_requests'

    def get_queryset(self):
        queryset = PurchaseRequest.objects.select_related('project', 'requested_by__user', 'approved_by__user').order_by('-created_at')
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(
                Q(purpose__icontains=query)
                | Q(project__name__icontains=query)
                | Q(requested_by__user__first_name__icontains=query)
                | Q(requested_by__user__last_name__icontains=query)
                | Q(requested_by__user__username__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '').strip()
        return context


class PurchaseRequestDetailView(FinanceOfficerRequiredMixin, DetailView):
    template_name = 'finance/purchaserequest_detail.html'
    context_object_name = 'purchase_request'
    queryset = PurchaseRequest.objects.select_related('project', 'requested_by__user', 'approved_by__user')


class PurchaseRequestCreateView(FinanceOfficerRequiredMixin, ExtraContextMixin, CreateView):
    model = PurchaseRequest
    form_class = PurchaseRequestCreateForm
    template_name = 'portal/object_form.html'
    title = 'New Purchase Request'
    success_url = reverse_lazy('portal:finance:purchase-request-list')

    def form_valid(self, form):
        form.instance.requested_by = Member.objects.filter(user=self.request.user).first()
        return super().form_valid(form)


class PurchaseRequestUpdateView(FinanceOfficerRequiredMixin, ExtraContextMixin, UpdateView):
    model = PurchaseRequest
    form_class = PurchaseRequestUpdateForm
    template_name = 'portal/object_form.html'
    title = 'Edit Purchase Request'

    def form_valid(self, form):
        if form.instance.status in ('APPROVED', 'REJECTED') and form.instance.approved_by_id is None:
            form.instance.approved_by = Member.objects.filter(user=self.request.user).first()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('portal:finance:purchase-request-detail', args=[self.object.pk])


class PurchaseRequestDeleteView(FinanceOfficerRequiredMixin, ExtraContextMixin, DeleteView):
    model = PurchaseRequest
    template_name = 'portal/object_confirm_delete.html'
    success_url = reverse_lazy('portal:finance:purchase-request-list')
