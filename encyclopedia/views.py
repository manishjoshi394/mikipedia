from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django import forms
from . import util
import markdown2
import logging

class NewEntryForm(forms.Form):
    title = forms.CharField(label = '', widget=forms.TextInput(attrs={'placeholder' : 'Title'}))
    content = forms.CharField(label = '', widget=forms.Textarea(attrs={'placeholder' : 'Content'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def render_entry(request, title):
    entry = util.get_entry(title)
    if (entry is None):
        return render(request, 'encyclopedia/error.html', {
            'title' : title,
            'error_title' : 'Not found',
            'error_msg' : 'Oops, there is no article with that title.'
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

def save_form(request, editing):
    form = NewEntryForm(request.POST)
    if form.is_valid():
        title = form.cleaned_data['title']
        content = form.cleaned_data['content']
        if editing or not util.get_entry(title):
            util.save_entry(title, content)
            return redirect(render_entry, title)
        else:
            return render(request, 'encyclopedia/error.html', {
                'title' : title,
                'error_title' : 'An article with this name already exists'
            })
    else:
        return render(request, 'encyclopedia/add.html', {
            'form' : form
        })    

def add_entry(request):
    if (request.method == 'POST'):
        return save_form(request, editing=False)
        
    return render(request, 'encyclopedia/add.html', {
        'form' : NewEntryForm()
    })

def edit_entry(request):
    if (request.method == 'POST'):
        return save_form(request, editing=True)
    title = request.GET.get('q')
    content = util.get_entry(title)
    form = NewEntryForm(initial={'title': title, 'content': title})
    form.fields['title'].widget.attrs['readonly'] = True
    return render(request, 'encyclopedia/add.html', {
        'form' : form
    })

