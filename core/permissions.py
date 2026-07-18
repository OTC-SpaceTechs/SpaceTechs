from functools import wraps

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
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

# Per PLAN.md Phase 6: finance views are restricted to this subset of officers.
FINANCE_OFFICER_GROUPS = ["Treasurer", "Chair", "Vice-Chair"]


def is_officer(user):
    return user.is_authenticated and user.groups.filter(name__in=OFFICER_GROUPS).exists()


def is_finance_officer(user):
    return user.is_authenticated and user.groups.filter(name__in=FINANCE_OFFICER_GROUPS).exists()


def _require(request, check_func, message):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
    if not check_func(request.user):
        raise PermissionDenied(message)
    return None


def officer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        denied = _require(request, is_officer, "This page is restricted to club officers.")
        if denied:
            return denied
        return view_func(request, *args, **kwargs)
    return wrapper


def finance_officer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        denied = _require(request, is_finance_officer, "This page is restricted to the Treasurer, Chair, and Vice-Chair.")
        if denied:
            return denied
        return view_func(request, *args, **kwargs)
    return wrapper


class OfficerRequiredMixin(AccessMixin):
    """CBV equivalent of @officer_required."""

    def dispatch(self, request, *args, **kwargs):
        denied = _require(request, is_officer, "This page is restricted to club officers.")
        if denied:
            return denied
        return super().dispatch(request, *args, **kwargs)


class FinanceOfficerRequiredMixin(AccessMixin):
    """CBV equivalent of @finance_officer_required."""

    def dispatch(self, request, *args, **kwargs):
        denied = _require(request, is_finance_officer, "This page is restricted to the Treasurer, Chair, and Vice-Chair.")
        if denied:
            return denied
        return super().dispatch(request, *args, **kwargs)


class IsOfficer(BasePermission):
    def has_permission(self, request, view):
        return is_officer(request.user)
