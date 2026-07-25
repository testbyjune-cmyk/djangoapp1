"""
댓글/문장 저장소 추상화 (의존관계 역전).

호출부(뷰, 믹스인)는 `get_comment_store()`가 돌려주는 저장소가 어떤
구체 구현인지 몰라도 된다. 로컬 개발 환경에서는 Django ORM(SQLite 등
DATABASES 설정을 그대로 따름)을 기본 저장소로 쓰고, Vercel 프로젝트에
KV(Upstash Redis) 통합을 연결해 환경 변수가 채워지면 자동으로 실제
Vercel KV를 사용하도록 전환된다. 코드를 다시 배포할 필요 없이 Vercel
대시보드에서 KV 통합만 연결하면 그 즉시 실제 KV 백엔드로 바뀐다.

지원하는 환경 변수(둘 중 하나만 있어도 됨):
- KV_REST_API_URL / KV_REST_API_TOKEN
  (Vercel Marketplace에서 Upstash를 프로젝트에 연결하면 자동 주입)
- UPSTASH_REDIS_REST_URL / UPSTASH_REDIS_REST_TOKEN
  (Upstash 콘솔에서 직접 발급한 자격 증명을 쓰는 경우)
"""

from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Protocol

MAX_COMMENT_LENGTH = 280
MAX_ENTRIES_PER_PAGE = 200


class CommentStore(Protocol):
    def list(self, page_key: str) -> list[dict]: ...

    def create(self, page_key: str, text: str) -> dict: ...

    def delete(self, page_key: str, entry_id: str) -> bool: ...

    def count(self, page_key: str) -> int: ...


class DjangoCommentStore:
    """로컬 개발용 기본 저장소. KV 통합이 없을 때 자동으로 선택된다."""

    def _serialize(self, comment) -> dict:
        return {
            "id": str(comment.pk),
            "text": comment.text,
            "created_at": comment.created_at.isoformat(),
        }

    def list(self, page_key: str) -> list[dict]:
        from .models import Comment

        return [self._serialize(c) for c in Comment.objects.filter(page_key=page_key)[:50]]

    def create(self, page_key: str, text: str) -> dict:
        from .models import Comment

        comment = Comment.objects.create(page_key=page_key, text=text)
        return self._serialize(comment)

    def delete(self, page_key: str, entry_id: str) -> bool:
        from .models import Comment

        deleted, _ = Comment.objects.filter(page_key=page_key, pk=entry_id).delete()
        return deleted > 0

    def count(self, page_key: str) -> int:
        from .models import Comment

        return Comment.objects.filter(page_key=page_key).count()


class UpstashCommentStore:
    """Vercel KV(Upstash Redis)의 REST API를 직접 호출하는 실제 저장소."""

    def __init__(self, base_url: str, token: str):
        self._base_url = base_url.rstrip("/")
        self._token = token

    def _command(self, *args: str):
        import requests

        response = requests.post(
            self._base_url,
            headers={"Authorization": f"Bearer {self._token}"},
            json=list(args),
            timeout=5,
        )
        response.raise_for_status()
        return response.json().get("result")

    def _key(self, page_key: str) -> str:
        return f"comments:{page_key}"

    def list(self, page_key: str) -> list[dict]:
        raw_items = self._command("LRANGE", self._key(page_key), "0", "49") or []
        return [json.loads(item) for item in raw_items]

    def create(self, page_key: str, text: str) -> dict:
        entry = {
            "id": uuid.uuid4().hex,
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        key = self._key(page_key)
        self._command("LPUSH", key, json.dumps(entry, ensure_ascii=False))
        self._command("LTRIM", key, "0", str(MAX_ENTRIES_PER_PAGE - 1))
        return entry

    def delete(self, page_key: str, entry_id: str) -> bool:
        key = self._key(page_key)
        raw_items = self._command("LRANGE", key, "0", str(MAX_ENTRIES_PER_PAGE - 1)) or []
        for raw in raw_items:
            entry = json.loads(raw)
            if entry.get("id") == entry_id:
                self._command("LREM", key, "1", raw)
                return True
        return False

    def count(self, page_key: str) -> int:
        result = self._command("LLEN", self._key(page_key))
        return int(result or 0)


def _upstash_credentials() -> tuple[str, str] | None:
    url = os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    if url and token:
        return url, token
    return None


def is_kv_configured() -> bool:
    return _upstash_credentials() is not None


def get_comment_store() -> CommentStore:
    credentials = _upstash_credentials()
    if credentials:
        return UpstashCommentStore(*credentials)
    return DjangoCommentStore()
