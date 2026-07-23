import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .models import AppToggle
from .navigation import get_all_items, get_nav_items, is_app_enabled
from .progress import get_completed, toggle_complete


class HomeView(TemplateView):
    """튜토리얼 모듈 목록과 진행률을 보여주는 대시보드."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = [item for item in get_nav_items() if item.app_label != "core"]
        completed = get_completed(self.request)

        context["modules"] = [
            {"item": item, "completed": item.app_label in completed} for item in items
        ]
        context["completed_count"] = len([m for m in context["modules"] if m["completed"]])
        context["total_count"] = len(items)
        return context


class SettingsView(View):
    template_name = "core/settings.html"
    # core 자체는 항상 켜져 있어야 하므로 설정 목록에서 제외한다.
    NON_TOGGLEABLE_LABELS = {"core"}

    def get_toggleable_items(self):
        return [
            item
            for item in get_all_items()
            if item.app_label not in self.NON_TOGGLEABLE_LABELS
        ]

    def get(self, request, *args, **kwargs):
        apps = [
            {"item": item, "enabled": is_app_enabled(item.app_label)}
            for item in self.get_toggleable_items()
        ]
        return render(request, self.template_name, {"apps": apps})

    def post(self, request, *args, **kwargs):
        for item in self.get_toggleable_items():
            enabled = request.POST.get(f"enabled__{item.app_label}") == "on"
            AppToggle.objects.update_or_create(
                app_label=item.app_label,
                defaults={"display_name": item.label, "is_enabled": enabled},
            )
        messages.success(request, "설정이 저장되었습니다.")
        return redirect("core:settings")


class ToggleProgressView(View):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

        app_label = payload.get("app_label", "")
        if not app_label:
            return JsonResponse({"error": "app_label이 필요합니다."}, status=400)

        completed = toggle_complete(request, app_label)
        return JsonResponse({"completed": completed})
