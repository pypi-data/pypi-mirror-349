from django.db import models
from django.core.exceptions import ValidationError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from django.template import Template, RequestContext
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from wagtail.models import (
    Page,
    Orderable,
)
from wagtail.fields import (
    RichTextField,
)
from wagtail.contrib.routable_page.models import (
    RoutablePageMixin, path,
)
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    TitleFieldPanel,
)
from wagtail.admin.widgets.slug import SlugInput
from modelcluster.fields import ParentalKey
from datetime import datetime

from .settings import (
    PLACES_EXTEND_TEMPLATE,
    google_api_key,
)
from .util import (
    matcher,
)

# Create your models here.
class Place(Orderable):
    page = ParentalKey("places.PlacesPage", related_name="places", on_delete=models.CASCADE)
    name = models.CharField(max_length=255, help_text=_("What's the name of this place? I.E. 'New York City', 'Amsterdam'"))
    slug = models.SlugField(max_length=255, help_text=_("Slug of the place"), blank=False, null=False)
    place_id = models.CharField(max_length=255, help_text=_("(Optional) Google Place ID"), blank=True, null=True)
    address = models.CharField(max_length=255, help_text=_("Full address of the place"), blank=True, null=True)
    description = RichTextField(help_text=_("Description of the place"), blank=True, null=True, features=[
        "bold",
        "italic",
        "link",
        "ol",
        "ul",
        "hr",
        "ai",
        "document-link",
        "image",
        "embed",
    ])
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At"),
        help_text=_("The date and time the place was last updated."),
    )

    panels = [
        TitleFieldPanel("name", targets=["slug"]),
        FieldPanel("slug", widget=SlugInput),
        FieldRowPanel([
            FieldPanel("place_id"),
            FieldPanel("address"),
        ]),
        FieldPanel("description"),
    ]

    def clean(self):
        super().clean()

        if not self.place_id and not self.address:
            raise ValidationError(_("You must provide either a Place ID or an address"))
        
        if not self.slug:
            self.slug = slugify(self.name)

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        ordering = ["sort_order"]

class PlacesPage(RoutablePageMixin, Page):
    class ChangeFrequency(models.TextChoices):
        MONTHLY = "monthly", _("Monthly")
        WEEKLY = "weekly", _("Weekly")
        DAILY = "daily", _("Daily")
        NONE = "none", _("None")
        AUTO_CALC = "auto", _("Auto Calculate")

    template = "places/places_page.html"
    detail_template = "places/places_detail.html"
    # change_frequency = "monthly"
    search_description = None

    places: models.QuerySet[Place]

    sidebar_title = models.CharField(
        max_length=255,
        help_text=_("Title of the sidebar"),
        blank=True,
        null=True,
    )

    no_place_message = RichTextField(
        help_text=_("Message to display when no place is selected"),
        blank=True,
        null=True,
        features=[
            "bold",
            "italic",
            "link",
            "ol",
            "ul",
            "hr",
            "ai",
            "document-link",
            "image",
            "embed",
        ],
    )

    description = RichTextField(
        help_text=_("Description of the places"),
        blank=True,
        null=True,
        features=[
            "h2", "h3", "h4", "h5", "h6",
            "bold", "italic", "link", "ol",
            "ul", "hr", "ai",
            "document-link", "image", "embed",
        ],
    )
    seo_description_template = models.TextField(
        max_length=1000,
        help_text=_("SEO Description Template, Django template syntax is allowed."),
        blank=True,
        null=True,
    )
    seo_change_frequency = models.CharField(
        max_length=10,
        choices=ChangeFrequency.choices,
        default=ChangeFrequency.NONE,
        help_text=_(
            "SEO Change Frequency, this tells search engines how often the page is updated.\n"
            "If you want to exclude the change frequency, set it to 'None'."
        ),
    )
    seo_priority = models.PositiveSmallIntegerField(
        help_text=_(
            "SEO Priority, the higher the number, the higher the priority. (0-100)\n"
            "If you want to use the default priority, set it to 0.\n"
            "100 is the highest priority and is translated to 1.0 in the sitemap.xml.\n"
            "0 is the lowest priority and is translated to 0.1 in the sitemap.xml."
        ),
        default=100,
    )
    seo_priority_places = models.PositiveSmallIntegerField(
        help_text=_(
            "SEO Priority for Places, the higher the number, the higher the priority. (0-100)\n"
            "If you want to use the default priority, set it to 0.\n"
            "100 is the highest priority and is translated to 1.0 in the sitemap.xml.\n"
            "0 is the lowest priority and is translated to 0.1 in the sitemap.xml."
        ),
        default=100,
    )

    content_panels = Page.content_panels + [
        FieldPanel("description"),
        FieldPanel("no_place_message"),
        TitleFieldPanel("sidebar_title", targets=[], placeholder=_("Sidebar Title")),
        InlinePanel("places", heading=_("Sidebar Places"), label=_("Place")),
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel("seo_description_template"),
        FieldPanel("seo_change_frequency"),
        FieldPanel("seo_priority"),
        FieldPanel("seo_priority_places"),
    ]

    class Meta:
        verbose_name = _("Places Page")
        verbose_name_plural = _("Places Pages")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_place = None

    @classmethod
    def calculate_seo_priority(cls, priority: int) -> str:
        return round(0.1 + (priority / 100) * 0.9, 2)

    def places_search_description(self, place: Place, request: HttpRequest):
        if self.seo_description_template and place:
            template = Template(
                self.seo_description_template,
            )
            context = RequestContext(request, {
                "page": self,
                "place": place,
            })
            
            text = template.render(
                context,
            )
            return text.strip()
        
        return super().search_description

    def get_context(self, request, *args, **kwargs):
        return super().get_context(request, *args, **kwargs) | {
            "EXTEND_TEMPLATE": PLACES_EXTEND_TEMPLATE,
            "places": self.places.all(),
            "is_canonical": True,
        }

    @path("<slug:slug>/", name="places_detail")
    def places_detail(self, request, slug):
        place = get_object_or_404(
            self.places, slug=slug,
        )

        self.current_place = place

        context = {
            "place": place,
            "google_maps_api_key": google_api_key(
                request,
            ),
            "extra_title": place.name,
            "hide_canonical_tag": True,
            "is_canonical": True,
        }

        self.search_description = self.places_search_description(
            place, request,
        )

        if hasattr(request, "is_htmx") and request.is_htmx or\
                request.headers.get("HX-Request") == "true":
            
            # Render the detail (htmx partial) template.
            response = self.render(
                request,
                context_overrides=context,
                template=self.detail_template,
            )
            response.headers["HX-Trigger"] = "places-changed"
            return response

        # Render the full page template.
        # 
        # This is necessary to render the full page template when the user
        # navigates to the page directly
        return self.render(
            request,
            context_overrides=context
        )

    # Calculate the change frequency of the page.
    # 
    # This is useful for sitemaps.
    def calc_changefreq(self, page: "PlacesPage"):
        freq = getattr(page, "change_frequency", None)
        if freq:
            return freq
        
        if page.seo_change_frequency == PlacesPage.ChangeFrequency.NONE:
            return None
        
        if page.seo_change_frequency != PlacesPage.ChangeFrequency.AUTO_CALC:
            return page.seo_change_frequency

        freqlist: list[datetime] = list(page.revisions.values_list("created_at", flat=True))
        if not freqlist:
            return "monthly"
        
        if len(freqlist) == 1:
            return "monthly"
        
        freqlist.sort()
        freqlist.reverse()
        delta = freqlist[0] - freqlist[-1]

        return str(matcher(delta.days, lambda days, cmp: days < cmp, (
                (1, "daily"),
                (7, "weekly"),
                (30, "monthly"),
                (365, "yearly"),
            ), default="monthly"))

    # Get the sitemap urls for the page.
    # 
    # This tells Wagtail what urls to include in the sitemap.
    def get_sitemap_urls(self, request = None, priority_mul = 1.0, get_translations = True):
        urls = []

        if not self.live:
            return urls

        full_url = self.get_full_url(request=request)

        sitemap_item = {
            "location": full_url,
            "lastmod": self.latest_revision_created_at,
            # "priority": f"{priority_mul:.1f}",
        }

        change_freq = self.calc_changefreq(
            self,
        )

        if change_freq:
            sitemap_item["changefreq"] = change_freq

        if self.seo_priority:
            p = PlacesPage.calculate_seo_priority(self.seo_priority_places)
            p = p * priority_mul
            sitemap_item["priority"] = f"{p:.1f}"

        urls.append(sitemap_item)

        places = self.places.all()
        for place in places:
            places_sitemap_item = {
                "location": f"{full_url}{place.slug}/",
                "lastmod": place.updated_at,
                # "priority": f"{(0.9 * priority_mul):.1f}",
            }

            if change_freq:
                places_sitemap_item["changefreq"] = change_freq

            if self.seo_priority_places:
                priority = PlacesPage.calculate_seo_priority(
                    self.seo_priority_places
                )
                priority = priority * priority_mul
                places_sitemap_item["priority"] = f"{priority:.1f}"

            urls.append(places_sitemap_item)

        if get_translations:
            for page in self.get_translations(inclusive=False)\
                    .live()\
                    .public():
                page: "PlacesPage"

                translated_sitemap_urls = page.get_sitemap_urls(
                    request=request,
                    priority_mul=0.8,
                    get_translations=False,
                )

                urls.extend(
                    translated_sitemap_urls,
                )

        return urls

