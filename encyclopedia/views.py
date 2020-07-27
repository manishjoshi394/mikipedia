from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_entry(request, title):
    entry = util.get_entry(title)
    if (entry is None):
        return render(request, 'encyclopedia/notfound_error.html', {
            'title' : title
        })
    return render(request, 'encyclopedia/entry.html', {
        'content' : markdown2.markdown(entry),
        'title' : title
    })

def render_search(request):
    keyword = request.GET.get('q')
    if (keyword == None):
        return redirect(index)

    all_entries = util.list_entries()
    if (keyword in all_entries):
        return redirect(render_entry, keyword)

    results = [title for title in all_entries if keyword in title]

    return render(request, 'encyclopedia/search.html', {
        'results' : results,
        'keyword' : keyword
    })

    
    

