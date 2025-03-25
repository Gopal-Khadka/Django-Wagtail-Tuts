from django.db import models
from datetime import date
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
        articles = ArticlePage.objects.live().order_by("-first_published_at")
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
