"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

if os.environ.get("VERCEL"):
    # /tmp is the only writable path in the serverless function; rebuild the
    # sqlite db there (schema + seed data) on cold start if it isn't present.
    from django.conf import settings
    from django.core.management import call_command

    db_path = Path(settings.DATABASES["default"]["NAME"])
    if not db_path.exists():
        call_command("migrate", run_syncdb=True, verbosity=0)
