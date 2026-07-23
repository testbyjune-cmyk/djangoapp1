from django.contrib import messages
from django.shortcuts import redirect

from .navigation import is_app_enabled


class AppToggleMiddleware:
    """설정에서 꺼진 앱의 URL에 직접 접근하면 홈으로 돌려보낸다."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        match = request.resolver_match
        app_label = match.app_name if match else ""
        if app_label and not is_app_enabled(app_label):
            messages.warning(request, "현재 꺼져 있는 기능입니다. 설정에서 다시 켤 수 있습니다.")
            return redirect("core:home")
        return None
