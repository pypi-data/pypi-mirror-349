from django.conf import settings as django_settings
from django.utils.module_loading import import_string
import logging

logger = logging.getLogger(__name__)

PLACES_RETRIEVE_GOOGLE_API_KEY = getattr(django_settings, "PLACES_RETRIEVE_GOOGLE_API_KEY", None)

# The template to extend for the places app.
# By default, this is "base.html".
# The base template should include the following blocks:
# - extra_css
# - extra_js
# - content
PLACES_EXTEND_TEMPLATE = getattr(django_settings, "PLACES_EXTEND_TEMPLATE", "base.html")

if PLACES_RETRIEVE_GOOGLE_API_KEY is None:
    logger.warning("PLACES_RETRIEVE_GOOGLE_API_KEY is not set. Places will not work properly.")
    PLACES_RETRIEVE_GOOGLE_API_KEY = lambda request: None
else:
    PLACES_RETRIEVE_GOOGLE_API_KEY = import_string(PLACES_RETRIEVE_GOOGLE_API_KEY)
    
def google_api_key(request):
    if not PLACES_RETRIEVE_GOOGLE_API_KEY:
        return None
    
    return PLACES_RETRIEVE_GOOGLE_API_KEY(request)