from django.urls import path,include
from . import views
app_name = 'chatbot'

urlpatterns = [
    path('',views.home,name="home"),
    path('Display-user/',views.displayUser,name="display-user"),
    path('connect/<str:pk>',views.sendUserChatRequest,name="connect-user"),
    path('chat/',views.getRoom,name="room"),
]