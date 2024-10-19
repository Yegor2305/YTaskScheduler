from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, SignInForm
from .models import User

# Create your views here.
def sign_in(request):
    if request.method == "POST":
        form = SignInForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data["login"]
            password = form.cleaned_data["password"]
            user = authenticate(request, login=login_input, password=password)
            if user is not None:
                login(request, user)
                return redirect('account')
            else:
                form.add_error(None, "Invalid login or password")
                
    else:
        form = SignInForm()
    return render(request, 'accounts/sign_in.html', {"form": form})

def sign_up(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("sign-in")

    else:
        form = SignUpForm()

    return render(request, 'accounts/sign_up.html', {"form": form})
