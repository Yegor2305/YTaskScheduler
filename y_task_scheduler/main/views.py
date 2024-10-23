from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse
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

    current_time = dt.datetime.now()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        action = request.GET.get("action")
        try:
            task = get_object_or_404(Task, id=signing.loads(request.GET.get("task_id")))
        except signing.BadSignature:
            raise Http404("Task not found")
        date = task.date

        if action == "change_task_state" or action == "delete":
              
            if action == "change_task_state":
                task.is_completed = not task.is_completed
                task.save()
            if action == "delete":
                task.delete()
          
            tasks = get_tasks(request.user, date)
            
            html = render_to_string('main/today_tasks_container_content.html', {'tasks': tasks, 'date': date})
            return HttpResponse(html)
        else:
            if action == "show":
                html = render_to_string('main/choosen_task_container_content.html', 
                                        {'choosen_task': task, "current_time": current_time, "date": date})
                return HttpResponse(html)
    else:
        date = request.GET.get("date")
        date = dt.datetime.strptime(date, '%Y-%m-%d').date() if date else dt.date.today()
        try:
            tasks = get_tasks(request.user, date)
        except:
            pass
        context = {
            "title": f"{request.user} | Tasks",
            "user": request.user,
            "tasks": tasks,
            "choosen_task": tasks[0] if tasks else None,
            "date": date,
            "current_time": current_time
        }
                
    return render(request, 'main/tasks.html', context=context)

def another(request):
    return render(request, 'main/about.html', {"title": "About"})

def get_tasks(user, date):
    try:
        tasks = Task.objects.filter(user = user, date = date).order_by("is_completed", "priority")
    except:
        return None
    
    return tasks