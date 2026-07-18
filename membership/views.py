from django.shortcuts import render

from core.permissions import officer_required

from .models import Member


@officer_required
def member_list(request):
    members = Member.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    return render(request, 'membership/member_list.html', {'members': members})
