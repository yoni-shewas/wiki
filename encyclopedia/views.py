from django.shortcuts import render
from django.http import HttpResponse
import markdown2


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def encyclopedia(request, TITLE):
    content = util.get_entry(TITLE)

    # Check if content is None
    if content is None:

        return render(request, "encyclopedia/pages.html",
                      {"title": TITLE, "content": html_content})

    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/pages.html",
                  {"title": TITLE, "content": html_content})
