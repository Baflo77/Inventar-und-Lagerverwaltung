from django.shortcuts import redirect
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings


class MitarbeiterLoginRequiredMiddleware:
    WHITELIST_PREFIXES = (
        "/login/",
        "/logout/",
        "/admin/",
        "/api/swagger/",
        "/auth/",
        "/static/",
        "/media/",
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path.startswith(self.WHITELIST_PREFIXES):
            return self.get_response(request)

        user = request.user

        if not user.is_authenticated:
            login_url = reverse("login")
            next_url = request.get_full_path()
            if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(f"{login_url}?next={next_url}")
            return redirect(login_url)

        if not user.groups.filter(name="Mitarbeiter").exists():
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Kein Zugriff: Nur Mitarbeiter dürfen diese Seite nutzen.")

        return self.get_response(request)
