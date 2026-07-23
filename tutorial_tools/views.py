from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class ToolsLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_tools/lesson.html"
    app_label = "tutorial_tools"
    module_title = "핵심 도구"
    module_icon = "🛠️"
