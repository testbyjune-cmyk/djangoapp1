"""
튜토리얼 레슨 화면들이 공유하는 진행 상태 계산 (이전/다음 모듈, 스텝 번호, 완료 여부).

각 튜토리얼 앱은 이 믹스인을 상속해 app_label/module_title/module_icon만
지정하면 되고, 순서 계산·완료 체크 로직은 core가 한 곳에서 관리한다.
"""

from .comment_ownership import owned_comment_ids
from .comment_store import get_comment_store
from .navigation import get_nav_items
from .progress import get_completed


class TutorialStepMixin:
    app_label: str = ""
    module_title: str = ""
    module_icon: str = "📘"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        items = [item for item in get_nav_items() if item.app_label != "core"]
        idx = next(
            (i for i, item in enumerate(items) if item.app_label == self.app_label), -1
        )

        owned = owned_comment_ids(self.request, self.app_label)
        comments = get_comment_store().list(self.app_label)
        for comment in comments:
            comment["can_delete"] = comment["id"] in owned

        context.update(
            {
                "prev_item": items[idx - 1] if idx > 0 else None,
                "next_item": items[idx + 1] if 0 <= idx < len(items) - 1 else None,
                "step_index": idx + 1 if idx >= 0 else 1,
                "step_total": len(items) or 1,
                "module_app_label": self.app_label,
                "module_title": self.module_title,
                "module_icon": self.module_icon,
                "is_completed": self.app_label in get_completed(self.request),
                "page_comments": comments,
                "page_comment_key": self.app_label,
            }
        )
        return context
