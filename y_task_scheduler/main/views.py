from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import signing
from django.http import JsonResponse
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
        tasks = Task.objects.filter(user = request.user).order_by("priority") #, date = date.today()
    except:
        pass

    context = {
        "title": f"{request.user} | Tasks",
        "user": request.user,
        "tasks": tasks,
        "choosen_task": tasks[0] if tasks else None,
        "date": date.today()
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        action = request.GET.get("action")
        try:
            task = get_object_or_404(Task, id=signing.loads(request.GET.get("task_id")))
        except signing.BadSignature:
            raise Http404("Task not found")
        
        if action == "delete":
            task.delete()
            return JsonResponse({'status': 'success'})
        if action == "show":
            if context["choosen_task"] != task:
                context["choosen_task"] = task
                
    return render(request, 'main/tasks.html', context=context)

def another(request):
    return render(request, 'main/about.html', {"title": "About"})