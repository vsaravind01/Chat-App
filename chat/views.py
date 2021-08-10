from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    if request.method == "POST":
        if request.POST.get('create', 'join') == "Create":
            return render(request, 'create_room.html')
        else:
            return render(request, 'room.html', {'room': request.POST.get('room')})
    return render(request, 'home.html')