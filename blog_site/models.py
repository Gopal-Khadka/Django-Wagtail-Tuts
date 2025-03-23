from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.search import index


class BlogPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]

    template = "blog_site/blog_page.html"
