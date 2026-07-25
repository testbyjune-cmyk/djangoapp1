"""세션 기반 댓글 소유권 추적 (로그인 없이 '내가 쓴 댓글'만 지울 수 있게 한다)."""

SESSION_KEY = "owned_comments"


def owned_comment_ids(request, page_key: str) -> set:
    owned = request.session.get(SESSION_KEY, {})
    return set(owned.get(page_key, []))


def remember_owned_comment(request, page_key: str, entry_id: str) -> None:
    owned = request.session.get(SESSION_KEY, {})
    ids = owned.get(page_key, [])
    ids.append(entry_id)
    owned[page_key] = ids
    request.session[SESSION_KEY] = owned


def forget_owned_comment(request, page_key: str, entry_id: str) -> None:
    owned = request.session.get(SESSION_KEY, {})
    ids = owned.get(page_key, [])
    if entry_id in ids:
        ids.remove(entry_id)
        owned[page_key] = ids
        request.session[SESSION_KEY] = owned
