from django.db import models


class GuestbookEntry(models.Model):
    """댓글(문장) 남기기 데모용 모델 - Vercel KV 같은 텍스트 저장소를 흉내낸다."""

    text = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.text[:30]
