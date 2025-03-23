# Django Wagtails Tuts

## Packages
- "django>=5.1.7": for backend
- "django-allauth>=65.5.0": For email auth
- "django-cleanup>=9.0.0": for cleaning up unnecessary fields in DB
- "django-cotton>=2.0.1": for using components
- "django-htmx>=1.23.0": For handling htmx ajax requets in views
- "wagtail>=6.4.1": For Content Management System


## Process 
1. **Using Wagtail Page Model**
```python
class BlogPage(Page):
    body = RichTextField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]

    template = "blog_site/blog_page.html"
```

Each page type *(a.k.a. content type)* in Wagtail is represented by a Django model. All page models must inherit from the `wagtail.models.Page` class. As all page types are Django models, you can use any field type that Django provides. Wagtail also provides `wagtail.fields.RichTextField` which provides a WYSIWYG editor for editing rich-text content.  

`body` is a `RichTextField`, a special Wagtail field. When *blank=True*, it means the field isn’t mandatory and you can leave it empty. You can use any of the Django core fields. `content_panels` define the capabilities and the layout of the editing interface. Adding fields to `content_panels` enables you to edit them in the Wagtail admin interface.  

**Summary**:
- Page Model: A class that defines a specific type of page in Wagtail, including its fields and behavior.
- content_panels: A list that specifies how the fields of the page model are displayed in the Wagtail admin interface, allowing for customization of the editing experience.

2. **Adding child page**
- New page model `ArticlePage` is added to models.py
- New `Blog` is added as `root` page and new `article` is nested under it.
- Respective templates are added to the `blog_site` folder under `templates` directory.
- Pages are made dynamic using  `variable` objects i.e `page` which represents the instance of model.
  
In the article page, all the contents are displayed as article. Refer t `article_page.html` for more.