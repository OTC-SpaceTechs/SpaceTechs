from .permissions import is_officer


def officer_context(request):
    return {'is_officer': is_officer(request.user)}
