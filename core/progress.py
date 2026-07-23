"""세션 기반 튜토리얼 진행률 추적 (로그인 없이 완료 상태를 기억)."""

SESSION_KEY = "completed_modules"


def get_completed(request) -> set:
    return set(request.session.get(SESSION_KEY, []))


def toggle_complete(request, app_label: str) -> bool:
    completed = get_completed(request)
    if app_label in completed:
        completed.discard(app_label)
        done = False
    else:
        completed.add(app_label)
        done = True
    request.session[SESSION_KEY] = list(completed)
    return done
