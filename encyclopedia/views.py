from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django import forms
from . import util
import markdown2

class NewEntryForm(forms.Form):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)

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

def add_entry(request):
    if (request.method == 'POST'):
        form = NewEntryForm(request.POST)
        if (form.is_valid()):
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
        else:
            return render(request, 'encyclopedia/add.html', {
                'form' : form
            })    
        
    return render(request, 'encyclopedia/add.html', {
        'form' : NewEntryForm()
    })
    

