import json

from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin

from .models import GuestbookEntry

MAX_LENGTH = 280
OWNED_SESSION_KEY = "owned_guestbook_entries"


def _serialize(entry: GuestbookEntry, owned_ids: set) -> dict:
    return {
        "id": entry.id,
        "text": entry.text,
        "created_at": entry.created_at.isoformat(),
        "can_delete": entry.id in owned_ids,
    }


class StorageLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_storage/lesson.html"
    app_label = "tutorial_storage"
    module_title = "Vercel 스토리지 (Blob & KV)"
    module_icon = "🪣"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owned_ids = set(self.request.session.get(OWNED_SESSION_KEY, []))
        entries = GuestbookEntry.objects.all()[:50]
        context["guestbook_entries"] = [_serialize(entry, owned_ids) for entry in entries]
        context["guestbook_total"] = GuestbookEntry.objects.count()
        context["guestbook_max_length"] = MAX_LENGTH
        return context


class GuestbookCreateView(View):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "잘못된 요청입니다."}, status=400)

        text = (payload.get("text") or "").strip()
        if not text:
            return JsonResponse({"error": "문장을 입력해주세요."}, status=400)
        if len(text) > MAX_LENGTH:
            return JsonResponse(
                {"error": f"{MAX_LENGTH}자를 초과했습니다 (현재 {len(text)}자)."},
                status=400,
            )

        entry = GuestbookEntry.objects.create(text=text)

        if not request.session.session_key:
            request.session.save()
        owned_ids = request.session.get(OWNED_SESSION_KEY, [])
        owned_ids.append(entry.id)
        request.session[OWNED_SESSION_KEY] = owned_ids

        return JsonResponse(
            {
                "entry": _serialize(entry, set(owned_ids)),
                "total": GuestbookEntry.objects.count(),
            },
            status=201,
        )


class GuestbookDeleteView(View):
    def post(self, request, pk, *args, **kwargs):
        owned_ids = set(request.session.get(OWNED_SESSION_KEY, []))
        if pk not in owned_ids:
            return JsonResponse({"error": "본인이 남긴 문장만 지울 수 있어요."}, status=403)

        deleted, _ = GuestbookEntry.objects.filter(pk=pk).delete()
        if deleted:
            owned_ids.discard(pk)
            request.session[OWNED_SESSION_KEY] = list(owned_ids)

        return JsonResponse({"total": GuestbookEntry.objects.count()})
