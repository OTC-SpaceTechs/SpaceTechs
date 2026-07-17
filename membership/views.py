from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

from .models import Member


@staff_member_required
def member_list(request):
    members = Member.objects.select_related('user').order_by('user__last_name', 'user__first_name')
    return render(request, 'membership/member_list.html', {'members': members})
