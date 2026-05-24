from django.urls import path
from . import views

urlpatterns = [

    path("", views.home),

    path("command/", views.handle_command),

]