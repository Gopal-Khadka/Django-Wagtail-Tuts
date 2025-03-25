from django.db import models
from datetime import date
from operator import attrgetter
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index

from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager


class BlogPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]

    template = "blog_site/blog_page.html"

    def get_context(self, request, *args, **kwargs):
        # You can use "articles" context in above defined template file
        context = super().get_context(request)
        tag = request.GET.get("tag")
        articles = ArticlePage.objects.live()
        # reversing the articles by "first_published_at" attribute
        articles = sorted(articles, key=attrgetter("first_published_at"), reverse=True)
        if tag:
            articles = articles.filter(tags__name=tag)
            context["tag"] = tag
        context["articles"] = articles
        return context


class ArticlePage(Page):
    intro = models.CharField(max_length=80)
    body = RichTextField(blank=True)
    date = models.DateField("Post date", default=date.today)
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.SET_NULL, null=True, related_name="+"
    )  # "+" sign indicates prevention of reverse relation
    # SO you can't find related articles from the image
    caption = models.CharField(blank=True, max_length=80)
    tags = ClusterTaggableManager(through="ArticleTag", blank=True)
    views = models.PositiveIntegerField(default=0, editable=False)

    def serve(self, request, *args, **kwargs):
        # This method is called each time when page is served
        session_key = f"article_viewed_{self.pk}"  # set session cookie to prevent re-increment in views

        if not request.session.get(session_key, False):
            # check if the session cookie is already set before
            self.increment_view_count()
            request.session[session_key] = True

        return super().serve(request, *args, **kwargs)

    def image_url(self):
        # for image to be shown in twitter card when user shares the article
        return self.image.get_rendition("fill-1200x675|jpegquality-80").url

    def increment_view_count(self):
        self.views += 1
        self.save(update_fields=["views"])  # only update views field

    def get_author(self):
        return self.owner.get_full_name()

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
        index.SearchField("tags"),
        index.SearchField("get_author"),
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("date"),
        FieldPanel("tags"),
    ]
    template = "blog_site/article_page.html"


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        ArticlePage, on_delete=models.CASCADE, related_name="tagged_items"
    )
