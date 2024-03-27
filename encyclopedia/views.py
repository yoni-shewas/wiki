from django.shortcuts import render
from django.http import HttpResponse
import markdown2
import re

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def encyclopedia(request, TITLE):
    content = util.get_entry(TITLE)

    if content is None:
        return render(request, "encyclopedia/pageNotFound.html")

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/pages.html",
                  {"title": TITLE, "content": html_content})


def query(request):
    title = request.GET.get('q')

    if title is None:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

    content = util.get_entry(title)
    contents = []

    if content is None:
        entryList = util.list_entries()

        pattern = re.compile(re.escape(title), re.IGNORECASE)

        for entry in entryList:
            if pattern.search(entry):
                contents.append(entry)

        if contents:
            return render(request, "encyclopedia/search.html", {
                "content": contents,
                "title": title
            })
        return render(request, "encyclopedia/search.html", {
            "content": contents,
            "title": title
        })

    return render(request, "encyclopedia/pages.html",
                  {"title": title, "content": content})
