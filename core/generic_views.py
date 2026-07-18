class ExtraContextMixin:
    """Adds a `title` and resolved `cancel_url` to Create/Update/Delete view context."""

    title = None
    cancel_url = None

    def get_title(self):
        return self.title

    def get_cancel_url(self):
        if self.cancel_url:
            return self.cancel_url
        # A plain `success_url` class attribute is safe to reuse directly. Calling
        # get_success_url() here is not: Django's default implementation does
        # self.object.__dict__ formatting, which blows up on CreateView GET
        # requests (self.object is None before the form is ever submitted).
        static_success_url = getattr(self, 'success_url', None)
        if static_success_url:
            return static_success_url
        return self.get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_title()
        context['cancel_url'] = self.get_cancel_url()
        return context
