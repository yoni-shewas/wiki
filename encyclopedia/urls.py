from django.urls import path
from . import views


urlpatterns = [
    path("", views.query, name="query"),
    path("", views.index, name="index"),
    path("encyclopedia/Create New Page/", views.newPage, name="newPage"),
    path("encyclopedia/<str:TITLE>/", views.encyclopedia, name="encyclopedia"),
]
