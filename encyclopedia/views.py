from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
import markdown2
from django import forms
from django.urls import reverse, include
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


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    MarkdownContent = forms.CharField(
        widget=forms.Textarea, label="Content")


def newPage(request):

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["MarkdownContent"]
            isTitle = util.get_entry(title)
            if isTitle is None:
                util.save_entry(title, content)
                html_content = markdown2.markdown(content)

                return render(request, "encyclopedia/pages.html",
                              {"title": title, "content": html_content})
            else:
                return HttpResponseForbidden("The requested Create was Forbidden duplicate exist.")
    return render(request, "encyclopedia/newPage.html", {
        "form": NewTaskForm()
    })
