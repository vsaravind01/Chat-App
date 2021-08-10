from django import forms

class RoomSearch(forms.Form):
    room = forms.CharField(label="Room", min_length=5, max_length=10, widget=forms.TextInput(
        attrs={
            'placeholder': "Search rooms..."
        }
    ))