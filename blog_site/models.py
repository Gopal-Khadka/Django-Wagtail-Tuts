from django.db import models
from datetime import date
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class BlogPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]

    template = "blog_site/blog_page.html"

    def get_context(self, request, *args, **kwargs):
        # You can use "articles" context in above defined template file
        articles = self.get_children().live().order_by("-first_published_at")
        context = super().get_context(request)
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
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
        FieldPanel("image"),
        FieldPanel("caption"),
        FieldPanel("date"),
    ]
    template = "blog_site/article_page.html"
