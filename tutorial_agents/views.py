from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class AgentsLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_agents/lesson.html"
    app_label = "tutorial_agents"
    module_title = "에이전트 & 서브에이전트"
    module_icon = "🤖"
