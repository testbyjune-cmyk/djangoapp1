from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class WorktreeLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_worktree/lesson.html"
    app_label = "tutorial_worktree"
    module_title = "워크트리 & 병렬 작업"
    module_icon = "🌳"
