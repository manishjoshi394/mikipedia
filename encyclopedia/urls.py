from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path('wiki/special:search', views.render_search, name="search"),
    path('wiki/<str:title>', views.render_entry, name="render_entry")
]
