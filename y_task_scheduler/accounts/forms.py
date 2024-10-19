from .models import User
from django.forms import ModelForm, TextInput, CharField, PasswordInput, Form

class SignInForm(Form):
    login = CharField(widget=TextInput(attrs={'placeholder': 'Login'}))
    password = CharField(widget=PasswordInput(attrs={'placeholder': 'Password'}))


class SignUpForm(ModelForm):
    repeat_password = CharField(
        widget = PasswordInput(attrs={'placeholder': 'Repeat password'}),
        strip = False,
    )
    class Meta:
        model = User
        fields = ["name", "last_name", "email", "login", "password"]
        widgets = {
            "name": TextInput(attrs={'placeholder': 'Name'}),
            "last_name": TextInput(attrs={'placeholder': 'Last name'}),
            "email": TextInput(attrs={'placeholder': 'Email'}),
            "login": TextInput(attrs={'placeholder': 'Login'}),
            "password": PasswordInput(attrs={'placeholder': 'Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        repeat_password = cleaned_data.get("repeat_password")

        if password and repeat_password and password != repeat_password:
            self.add_error('repeat_password', "Пароли не совпадают")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.normalize_all()
        if commit:
            user.save()
        return user