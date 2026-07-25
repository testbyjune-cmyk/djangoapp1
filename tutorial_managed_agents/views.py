from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class ManagedAgentsLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_managed_agents/lesson.html"
    app_label = "tutorial_managed_agents"
    module_title = "Managed Agent"
    module_icon = "☁️"
