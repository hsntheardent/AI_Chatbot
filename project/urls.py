from django.urls import path
from app.views import chat, chat_view, admin_panel, delete_faq

urlpatterns = [
    path("", chat_view),
    path("chat/", chat, name="chat"),

    # Admin panel
    path("admin-panel/", admin_panel, name="admin_panel"),
    path("delete-faq/<str:question>/", delete_faq, name="delete_faq"),]