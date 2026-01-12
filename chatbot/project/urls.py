from django.contrib import admin
from django.urls import path
from app.views import chat_view
from app.views import chat

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat_view, name='chat'),
    path('chat/', chat, name='chat'), 
]
 