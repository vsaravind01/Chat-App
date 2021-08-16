from django import forms


class RoomSearch(forms.Form):
    room = forms.CharField(label="Room", min_length=5, max_length=10, widget=forms.TextInput(
        attrs={
            'placeholder': "Search rooms..."
        }
    ))


class CreateRoom(forms.Form):
    room = forms.CharField(label="Room", min_length=5, max_length=10)
    admin = forms.CharField(label="Username", min_length=4, max_length=18)

