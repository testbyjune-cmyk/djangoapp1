from django.views.generic import TemplateView

from core.comment_ownership import owned_comment_ids
from core.comment_store import MAX_COMMENT_LENGTH, get_comment_store, is_kv_configured
from core.mixins import TutorialStepMixin

SENTENCE_PAGE_KEY = "sentence-demo"


class StorageLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_storage/lesson.html"
    app_label = "tutorial_storage"
    module_title = "Vercel 스토리지 (Blob & KV)"
    module_icon = "🪣"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        store = get_comment_store()
        owned = owned_comment_ids(self.request, SENTENCE_PAGE_KEY)
        entries = store.list(SENTENCE_PAGE_KEY)
        for entry in entries:
            entry["can_delete"] = entry["id"] in owned

        context["sentence_page_key"] = SENTENCE_PAGE_KEY
        context["sentence_entries"] = entries
        context["sentence_total"] = store.count(SENTENCE_PAGE_KEY)
        context["sentence_max_length"] = MAX_COMMENT_LENGTH
        context["kv_configured"] = is_kv_configured()
        return context
