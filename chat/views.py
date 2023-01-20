from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from .models import Room, Message
from .forms import RoomSearch, CreateRoom, CreateUser, LoginUser
from django.http import HttpResponse, HttpResponseNotFound


def signup(request):
    form = CreateUser()
    errors = []
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        if password != confirm_password:
            errors.append("Password confirmation do not match!")
            return render(request, 'signup.html', {'form': form, 'errors': errors})
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            return redirect('login')
        except:
            errors.append('username already exists!')
            return render(request, 'signup.html', {'form': form, 'errors': errors})
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginUser()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, 'login.html', {'form': form, 'error': "invalid credentials"})
    return render(request, 'login.html', {'form': form})


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def home(request):
    form = RoomSearch()
    if request.method == "POST":
        if request.POST.get('create', 'join') == "Create":
            return redirect('create')
        else:
            room_name = request.POST.get('room')
            if not Room.objects.filter(name=room_name).exists():
                return render(request, 'home.html', {'form': form, 'errors': [f"Room name '{room_name}' doesn't exist!"]})
            return redirect('room', room_name=request.POST.get('room'))
    return render(request, 'home.html', {'form': form})


@login_required(login_url="/login")
def room(request, room_name):
    try:
        room_data = Room.objects.get(name__exact=room_name)
        Messages = Message.objects.filter(room__name__exact=room_name)
        return render(request, 'room.html', {'room': room_data, 'messages': Messages})
    except:
        messages.info(request, "room name does not exist!")
        return redirect('home')


@login_required(login_url="/login")
def check(request):
    if request.method == "POST":
        room_name = request.POST.get('room')
        admin = request.POST.get('admin')

        if Room.objects.filter(name=room_name).exists():
            messages.error(request, 'Room already exists')
            return redirect('create', error="Room already exists")

        query = Room(name=room_name, admin=admin)
        query.save()

        messages.success(request, 'Student created successfully.')
        return redirect('room', room=room_name)


@login_required(login_url="/login")
def create(request):
    form = CreateRoom()
    if request.method == "POST":
        room_name = request.POST.get('room')
        admin = request.user.username
        try:
            new_room = Room.objects.create(name=room_name, admin=admin)
            new_room.save()
            return redirect('room', room_name=room_name)
        except:
            return render(request, 'create_room.html', {'form': form, 'errors': ['Room name already exists!']})
    return render(request, 'create_room.html', {'form': form})


