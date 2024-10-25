from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import signing
from .models import Task, Resource, TaskResources
from .forms import temp_resources_for_task as trft
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

        if action == "add_resource_for_task" or action == "remove_resource_from_task":
            resource = Resource.objects.get(id=signing.loads(request.GET.get("resource_id")))
            if action == "add_resource_for_task":
                resource_count = request.GET.get("resource_count")  
                trft[resource] = resource_count
            else:
                trft.pop(resource, None)
            return JsonResponse({
                "resources_label": ', '.join([f'{resource.name} ({quantity})' for resource, quantity in trft.items()])
                })
        
        task = None
        date = None
        if action != "add_task":
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
            if action == "add_task" or action == "edit_task":
                trft.clear()
                priorities = Task.PRIORITY_CHOICES
                groups = request.user.groups.all()
                resources = request.user.resources.all() 
                context = {
                    "resources": resources,
                    "priorities": priorities,
                    "groups": groups
                }                                                     
                if action == "edit_task":
                    task_resources = task.taskresources_set.all()
                    for task_res in task_resources:
                        trft[task_res.resource] = task_res.amount
                    context["task"] = task
                    context["task_resources"] = task_resources
                html = render_to_string(request=request, template_name='main/add_edit_task_card.html', context=context)
                return HttpResponse(html)
            
    else:
        if request.method == "POST":
            task = None
            name = request.POST.get("task-name")
            name = name if name.strip() != '' else "nameless task"
            group = request.POST.get("task-group-select")
            group = request.user.groups.get(id=signing.loads(group)) if group != "None" else None
            
            time_start = dt.datetime.strptime(request.POST.get("task-time-start"), "%H:%M").time() if request.POST.get("task-time-start") != '' else dt.datetime.now().time()
            time_end = dt.datetime.strptime(request.POST.get("task-time-end"), "%H:%M").time() if request.POST.get("task-time-end") != '' else time_start
            if time_start > time_end:
                time_start, time_end = time_end, time_start

            if request.POST.get("action") == "add_task":             
                task = Task(
                    name = name,
                    description = request.POST.get("task-description"),
                    priority = request.POST.get("task-priority-select"),
                    date = request.session.get("date"),
                    user = request.user,
                    time_start = time_start,
                    time_end = time_end,
                    group = group,
                )
                task.save()

            if request.POST.get("action") == "edit_task":
                task = get_object_or_404(Task, id=signing.loads(request.POST.get("task_id")))
                task.name = name
                task.description = request.POST.get("task-description")
                task.priority = request.POST.get("task-priority-select")
                task.group = group
                task.time_start = time_start
                task.time_end = time_end
                task.save()
                task.taskresources_set.all().delete()

            for resource, amount in trft.items():
                task_resource = TaskResources(
                    task = task,
                    resource = resource,
                    amount = amount
                )
                task_resource.save()

            return redirect("tasks")     
        else:
            date = request.GET.get("date")
            date = request.session.get("date") if not date else date
            date = dt.datetime.strptime(date, '%Y-%m-%d').date() if date else dt.date.today()
            request.session["date"] = date.strftime("%Y-%m-%d")
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