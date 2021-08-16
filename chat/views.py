from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Room, Message
from .forms import RoomSearch, CreateRoom
from django.http import HttpResponse, HttpResponseNotFound


def home(request):
    if request.method == "POST":
        if request.POST.get('create', 'join') == "Create":
            return redirect('create', error=" ")
        else:
            return redirect('room', room=request.POST.get('room'))
    form = RoomSearch()
    return render(request, 'home.html', {'form': form})


def room(request, room):
    return render(request, 'room.html', {'room': room})


def check(request):
    if request.method == "POST":
        room_name = request.POST.get('room')
        admin = request.POST.get('admin')

        if Room.objects.filter(name=room_name).exists():
            print(room_name)
            messages.error(request, 'Room already exists')
            return redirect('create', error="Room already exists")

        query = Room(name=room_name, admin=admin)
        query.save()

        messages.success(request, 'Student created successfully.')
        return redirect('room', room=room_name)


def create(request, error=" "):
    if error == " ":
        print("yes")
    else:
        print(error)
    form = CreateRoom()
    return render(request, 'create_room.html', {'error': error, 'form': form})
