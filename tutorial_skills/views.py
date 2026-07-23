from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class SkillsLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_skills/lesson.html"
    app_label = "tutorial_skills"
    module_title = "스킬 & 커스터마이징"
    module_icon = "🧩"
