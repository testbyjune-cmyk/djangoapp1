from django.db import models


class AppToggle(models.Model):
    """플러그인 앱의 활성/비활성 상태. 레코드가 없으면 기본값은 '활성'이다."""

    app_label = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["app_label"]

    def __str__(self):
        state = "ON" if self.is_enabled else "OFF"
        return f"{self.display_name} ({state})"
