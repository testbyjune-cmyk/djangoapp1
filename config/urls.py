from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("tutorial/agents/", include("tutorial_agents.urls")),
    path("tutorial/tools/", include("tutorial_tools.urls")),
    path("tutorial/worktree/", include("tutorial_worktree.urls")),
    path("tutorial/skills/", include("tutorial_skills.urls")),
]
