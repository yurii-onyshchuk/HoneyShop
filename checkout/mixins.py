from django.shortcuts import redirect


class AllowOnlyRedirectMixin:
    """Mixin to control access to a view based on the previous URL.

    This mixin checks the previous URL and allows or disallows access to
    a view based on specific conditions.
    """

    def get(self, request, *args, **kwargs):
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url:
            if str(self.allow_previous_url) in previous_url:
                return super().get(request, *args, **kwargs)
            if not self.allow_previous_url:
                return redirect(self.redirect_url)
        else:
            return redirect(self.redirect_url)
