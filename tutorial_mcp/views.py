from django.views.generic import TemplateView

from core.mixins import TutorialStepMixin


class McpLessonView(TutorialStepMixin, TemplateView):
    template_name = "tutorial_mcp/lesson.html"
    app_label = "tutorial_mcp"
    module_title = "MCP"
    module_icon = "🔌"
