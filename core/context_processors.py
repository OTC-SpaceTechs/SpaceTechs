from .permissions import is_finance_officer, is_officer


def officer_context(request):
    return {
        'is_officer': is_officer(request.user),
        'is_finance_officer': is_finance_officer(request.user),
    }
