from __future__ import annotations

from django.urls import path

from app import easter_eggs, views

urlpatterns = [
    path("", views.read_root, name="root"),
    path("eggs", easter_eggs.eggs, name="eggs"),
]
