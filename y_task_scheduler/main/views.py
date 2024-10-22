from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import signing
from django.http import JsonResponse
from .models import Task
import datetime as dt

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

    date = request.GET.get("date")

    date = dt.datetime.strptime(date, '%Y-%m-%d').date() if date else dt.date.today()

    try:
        tasks = Task.objects.filter(user = request.user, date = date).order_by("is_completed", "priority") #, date = date.today()
    except:
        pass

    if request.method == "POST":
        if (request.POST.get("request_name") == "change_task_state"):
            task_state = not request.POST.get("task_state")
            task = tasks.get(id=signing.loads(request.POST.get("task_id")))
            task.is_completed = not task_state
            task.save()
        return redirect("tasks")

    context = {
        "title": f"{request.user} | Tasks",
        "user": request.user,
        "tasks": tasks,
        "choosen_task": tasks[0] if tasks else None,
        "date": date
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
            data = {
                "name": task.name,
                "description": task.description
            }
            return JsonResponse(data)
                
    return render(request, 'main/tasks.html', context=context)

def another(request):
    return render(request, 'main/about.html', {"title": "About"})