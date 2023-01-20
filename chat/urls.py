from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name='home'),
    path("<str:room_name>/", views.room, name='room'),
    path("create", views.create, name='create'),
    path("check", views.check, name="check"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout")
]