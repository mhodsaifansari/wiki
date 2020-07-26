from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>",views.goto,name="goto"),
    path("newpage",views.newpage,name="newpage"),
    path("randompage",views.randompage,name="randompage"),
    path("edit/<str:name>",views.edit,name="edit")
]
