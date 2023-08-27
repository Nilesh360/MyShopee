from django.contrib import admin
from django.urls import path,include
import base
from base import views
import chatbot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/',include('base.urls')),
    path('chatbot/',include('chatbot.urls')),
    path('',views.home,name='home'),
]
