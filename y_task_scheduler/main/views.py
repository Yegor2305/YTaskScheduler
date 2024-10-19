from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.functional import SimpleLazyObject
from .models import User

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {"title": "Home"})

def log_out(request):
    print(request.user.is_authenticated)
    logout(request)
    print(request.user)
    return redirect('home')

@login_required
def personal_page(request):
    if request.user.is_superuser:
        return redirect("sign-in")

    return render(request, 'main/personal_page.html', {"title": f"{request.user} | Tasks", "user": request.user})

def another(request):
    return render(request, 'main/about.html', {"title": "About"})