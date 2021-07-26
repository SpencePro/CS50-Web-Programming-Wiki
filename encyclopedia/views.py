from typing import NoReturn
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django import forms
from django.urls import reverse
from . import util
from .models import Entry
import random
import re
import markdown2


class SearchForm(forms.Form):
    query = forms.CharField(min_length=1,
                            label='',
                            widget=forms.TextInput(attrs={
                                'size': '20',
                                'autocomplete': 'off',
                                'placeholder': 'Search Encyclopedia'
                            }
                            ))


class EditForm(forms.Form):
    article = forms.CharField(min_length=10,
                              label='',
                              widget=forms.Textarea(attrs={
                                  'autocomplete': 'off',
                                  'placeholder': 'Add Entry in Markdown'
                              }
                              ))


def index(request):
    context = {
        "entries": util.list_entries(),
        "form": SearchForm(),
    }
    return render(request, "encyclopedia/index.html", context)


def entry(request, title):
    if request.method in ["GET", "POST"]:
        titles = util.list_entries()
        if title in titles:
            context = {
                "title": title,
                "content": markdown2.markdown(util.get_entry(title)),
                "form": SearchForm(),
            }
            return render(request, "encyclopedia/entry.html", context)
        else:
            return HttpResponseRedirect(reverse('encyclopedia:error'))


def search(request):
    form = SearchForm(request.POST)
    matches = []
    if form.is_valid():
        query = form.cleaned_data["query"]
        entries = util.list_entries()
        # compile regex up here so it is cached, no need to recompile each iteration
        r = re.compile(rf"({query})", re.IGNORECASE)
        for entry in entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={"title": entry}))
            else:
                # if no exact match, run regex search, append matches to list, return list
                match = r.search(entry)
                if match:
                    matches.append(entry)
        # if we have any matches
        if len(matches) > 0:
            return render(request, "encyclopedia/search.html", {
                "entries": matches,
                "form": SearchForm(),
            })
        # if there are no matches
        else:
            return HttpResponseRedirect(reverse('encyclopedia:error'))


def random_page(request):
    entries = util.list_entries()
    rand = random.randint(0, len(entries)-1)
    title = entries[rand]
    return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={"title": title}))


def new(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            article = form.cleaned_data["article"]
            title = article.split("\n")[0].strip("#").strip()
            util.save_entry(title, article)
            obj = Entry(title=f"{title}", content=f"{article}")
            obj.save()
        return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={"title": title}))

    return render(request, "encyclopedia/new.html", {
        "form": SearchForm(),
        "edit_form": EditForm()
    })


def edit(request):
    if request.method == "POST":
        title = request.POST.get("edit").strip("Edit ")
        content = util.get_entry(title)
        initial = {'article': f'{content}'}
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "edit_form": EditForm(initial=initial),
            "form": SearchForm(),
        })


def save_edit(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            article = form.cleaned_data["article"]
            title = article.split("\n")[0].strip("#").strip()
            util.save_entry(title, article)
        return HttpResponseRedirect(reverse('encyclopedia:wiki', kwargs={"title": title}))


def error(request):
    return render(request, "encyclopedia/error.html", {
        "form": SearchForm(),
    })
