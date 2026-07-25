import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from .comment_ownership import forget_owned_comment, owned_comment_ids, remember_owned_comment
from .comment_store import MAX_COMMENT_LENGTH, get_comment_store
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


class CommentCreateView(View):
    """댓글/문장 남기기. page_key로 어느 콘텐츠에 다는 댓글인지 구분한다."""

    def post(self, request, page_key, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

        text = (payload.get("text") or "").strip()
        if not text:
            return JsonResponse({"error": "문장을 입력해주세요."}, status=400)
        if len(text) > MAX_COMMENT_LENGTH:
            return JsonResponse(
                {"error": f"{MAX_COMMENT_LENGTH}자를 초과했습니다 (현재 {len(text)}자)."},
                status=400,
            )

        store = get_comment_store()
        entry = store.create(page_key, text)

        if not request.session.session_key:
            request.session.save()
        remember_owned_comment(request, page_key, entry["id"])
        entry["can_delete"] = True

        return JsonResponse({"entry": entry, "total": store.count(page_key)}, status=201)


class CommentDeleteView(View):
    def post(self, request, page_key, entry_id, *args, **kwargs):
        if entry_id not in owned_comment_ids(request, page_key):
            return JsonResponse({"error": "본인이 남긴 문장만 지울 수 있어요."}, status=403)

        store = get_comment_store()
        deleted = store.delete(page_key, entry_id)
        if deleted:
            forget_owned_comment(request, page_key, entry_id)
        return JsonResponse({"deleted": deleted, "total": store.count(page_key)})
