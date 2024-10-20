from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import signing
from django.db import models
from .models import Task
from datetime import date

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
        logout(request=request)
        return redirect("sign-in")

    tasks = None
    try:
        tasks = Task.objects.filter(user = request.user, date = date.today()).order_by("priority")
    except:
        pass

    context = {
        "title": f"{request.user} | Tasks",
        "user": request.user,
        "tasks": tasks,
        "date": date.today()
    }

    return render(request, 'main/tasks.html', context=context)

@login_required
def delete_task(request, encrypted_id):
    try:
        task_id = signing.loads(encrypted_id)
    except signing.BadSignature:
        raise Http404("Task not found")
    
    task = get_object_or_404(Task, id=task_id)
        
    if task.user != request.user:
        raise Http404("Task not found")

    task.delete()
    return redirect('account')

def another(request):
    return render(request, 'main/about.html', {"title": "About"})