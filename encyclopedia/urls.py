from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>/", views.entry, name="wiki"),
    path("search/", views.search, name="search"),
    path("random/", views.random_page, name="random"),
    path("new/", views.new, name="new"),
    path("edit/", views.edit, name="edit"),
    path("save_edit/", views.save_edit, name="save_edit"),
    path("error/", views.error, name="error"),
]
