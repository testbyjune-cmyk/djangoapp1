from .navigation import get_nav_items


def navigation(request):
    return {"nav_items": get_nav_items()}
