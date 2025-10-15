from __future__ import annotations

from django.urls import path

from app import views

urlpatterns = [
    path("", views.read_root, name="root"),
]
