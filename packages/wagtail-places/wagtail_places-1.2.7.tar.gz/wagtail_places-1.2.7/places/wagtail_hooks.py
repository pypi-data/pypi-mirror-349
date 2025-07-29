from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from .models import Place

class PlaceViewSet(SnippetViewSet):
    model = Place

register_snippet(Place, viewset=PlaceViewSet)
