from django.db import models


class Comment(models.Model):
    """댓글/문장 저장 데모용 모델.

    Vercel KV(Upstash) 통합이 연결되지 않은 로컬 개발 환경에서
    DjangoCommentStore가 사용하는 기본(fallback) 저장소다.
    page_key로 어느 콘텐츠(튜토리얼 모듈)에 달린 댓글인지 구분한다.
    """

    page_key = models.CharField(max_length=100, db_index=True)
    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.page_key}] {self.text[:30]}"


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
