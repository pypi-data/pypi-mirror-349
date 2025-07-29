# django_debug_toolbar_query_assistant_panel/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("llm-chat/", views.llm_chat, name="llm_chat"),
    path("upload-context/", views.upload_context, name="upload_context"),
]