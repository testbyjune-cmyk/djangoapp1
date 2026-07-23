from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import RedirectView

from .models import AppToggle
from .navigation import get_all_items, is_app_enabled


class HomeView(RedirectView):
    pattern_name = "engineering_calculator:calculator"


class SettingsView(View):
    template_name = "core/settings.html"
    # 홈(기본) 앱과 core 자체는 항상 켜져 있어야 하므로 설정 목록에서 제외한다.
    NON_TOGGLEABLE_LABELS = {"core", "engineering_calculator"}

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
