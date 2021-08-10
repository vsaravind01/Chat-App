from django.shortcuts import render
from .forms import RoomSearch
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        if request.POST.get('create', 'join') == "Create":
            return render(request, 'create_room.html')
        else:
            print()
            return render(request, 'room.html', {'room': request.POST.get('room')})
    form = RoomSearch()
    return render(request, 'home.html', {'form': form})
