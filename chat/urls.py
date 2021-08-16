from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("<str:room>/", views.room, name='room'),
    path("create/<str:error>/", views.create, name='create'),
    path("check", views.check, name="check")
]