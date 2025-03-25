from django.shortcuts import render, redirect
from django.http import HttpRequest
from operator import attrgetter

from .models import ArticlePage


# Create your views here.
def article_search(request: HttpRequest):
    search_query = request.GET.get("query", "").strip()
    if not search_query:
        return redirect("/blog")
    articles = ArticlePage.objects.live().search(search_query)
    # reversing the articles by "first_published_at" attribute
    articles = sorted(articles, key=attrgetter("first_published_at"), reverse=True)

    context = {
        "articles": articles,
        "search_query": search_query,
    }
    return render(request, "blog_site/blog_page.html", context=context)
