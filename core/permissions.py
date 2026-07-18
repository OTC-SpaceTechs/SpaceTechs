from functools import wraps

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

# Keep in sync with core.migrations.0002_officer_groups.OFFICER_GROUPS
OFFICER_GROUPS = [
    "Chair",
    "Vice-Chair",
    "Secretary",
    "Treasurer",
    "Director of Projects",
    "Director of Research",
    "Director of Outreach",
    "SEDS Rep",
    "Member-at-large",
]


def is_officer(user):
    return user.is_authenticated and user.groups.filter(name__in=OFFICER_GROUPS).exists()


def officer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        if not is_officer(request.user):
            raise PermissionDenied("This page is restricted to club officers.")
        return view_func(request, *args, **kwargs)
    return wrapper


class IsOfficer(BasePermission):
    def has_permission(self, request, view):
        return is_officer(request.user)
