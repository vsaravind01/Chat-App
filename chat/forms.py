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


class CreateUser(forms.Form):
    username = forms.CharField(label="username", min_length=8, max_length=20)
    password = forms.CharField(label="password", widget=forms.PasswordInput())
    confirm_password = forms.CharField(label="confirm password", widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') == cleaned_data.get('confirm_password'):
            self.add_error('password confirm', 'passwords confirmation mismatch!')
        return self.cleaned_data


class LoginUser(forms.Form):
    username = forms.CharField(label="username", min_length=8, max_length=20)
    password = forms.CharField(label="password", widget=forms.PasswordInput())
