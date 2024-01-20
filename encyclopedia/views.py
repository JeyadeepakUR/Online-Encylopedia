from django.shortcuts import redirect, render
from markdown2 import markdown
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title.strip())
    if content == None:
        content = "Page Not Found"
    content = markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": content
    })
def search(request):
    q = request.GET.get('q').strip()
    if q in util.list_entries():
        return redirect("entry", title=q)
    return render(request, "encyclopedia/search.html", {"entries": util.search(q), "q": q})
def create(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) != None:
            return render(request, "encyclopedia/add.html", {
                "message": "Page already exists"
            })
        else:
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return render(request, "encyclopedia/add.html")
def edit(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        title = request.POST.get('title')
        if content == "":
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content,
                "message": "Content cannot be empty"
            })
        util.save_entry(title, content)
        return redirect("entry", title=title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })
def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    return entry(request, title)
