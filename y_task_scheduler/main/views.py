from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import Http404, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core import signing
from .models import Task, Resource, TaskResources, Color, Group
from .forms import temp_resources_for_task as trft
import datetime as dt

# Create your views here.
def index(request):
    return render(request, 'main/index.html', {"title": "Home"})

def log_out(request):
    logout(request)
    return redirect('home')

@login_required
def tasks_page(request):
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
            
            html = render_to_string('main/containers_content/today_tasks_container_content.html', {'tasks': tasks, 'date': date})
            return HttpResponse(html)
        else:
            if action == "show":
                html = render_to_string('main/containers_content/choosen_task_container_content.html', 
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

@login_required
def groups_and_resources_page(request):
    if request.user.is_superuser:
        logout(request=request)
        return redirect("sign-in")
    
    groups = request.user.groups.all()
    resources = request.user.resources.all()
    choosen_group = groups[0] if groups else None
    choosen_resource = resources[0] if groups else None
    context = {
        "title": "Groups & Resources",
        "groups": groups,
        "resources": resources, 
        "choosen_group": choosen_group,   
        "choosen_resource": choosen_resource,   
    }

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        action = request.GET.get("action")
        template_name = ""
        if action == "group_changed":
            context["choosen_group"] = groups.get(id=signing.loads(request.GET.get("group_id")))
            template_name = "main/containers_content/groups_container_content.html"

        if action == "edit_group" or action == "add_group" or action == "delete_group":
            if action == "edit_group":
                context["choosen_group"] = groups.get(id=signing.loads(request.GET.get("group_id")))
                context["action"] = "edit"
            elif action == "add_group":
                context.pop("choosen_group", None)
                context["action"] = "add"
            else:
                group = groups.get(id=signing.loads(request.GET.get("group_id")))
                group.delete()
                context["groups"] = request.user.groups.all()
                context["choosen_group"] = context["groups"][0]

            colors = Color.objects.all()
            context["colors"] = colors
            template_name = "main/containers_content/groups_container_content.html"
    
        if action == "resource_changed":
            template_name = "main/containers_content/resources_container_content.html"
            context["choosen_resource"] = resources.get(id=signing.loads(request.GET.get("resource_id")))

        if action == "edit_resource" or action == "add_resource" or action == "delete_resource":
            if action == "edit_resource":
                context["choosen_resource"] = resources.get(id=signing.loads(request.GET.get("resource_id")))
                context["action"] = "edit"
            elif action == "add_resource":
                context.pop("choosen_resource", None)
                context["action"] = "add"
            else:
                resource = resources.get(id=signing.loads(request.GET.get("resource_id")))
                resource.delete()
                context["resources"] = request.user.resources.all()
                context["choosen_resource"] = context["resources"][0]

            template_name = "main/containers_content/resources_container_content.html"

        html = render_to_string(request=request, template_name=template_name, context=context)
        return HttpResponse(html)
    else:
        if request.method == "POST":
            action = request.POST.get("action")

            if action == "edit_group" or action == "add_group":
                group = None
                name = request.POST.get("group-name")
                name = name if name.strip() != "" else "nameless" 
                description = request.POST.get("description")
                color = Color.objects.get(value=request.POST.get("color-select"))
                if action == "edit_group":
                    group_id = request.POST.get("group_id")
                    group = groups.get(id=signing.loads(group_id))       
                    group.name = name
                    group.description = description
                    group.color = color
                else:
                    group = Group(
                        name = name,
                        description = description,
                        color = color,
                        user = request.user
                    )
                group.save()

            if action == "edit_resource" or action == "add_resource":
                resource = None
                name = request.POST.get("resource-name")
                name = name if name.strip() != "" else "nameless" 
                description = request.POST.get("description")
                price = float(request.POST.get("price"))
                price = price if price >= 0 else 0
                if action == "edit_resource":
                    resource_id = request.POST.get("resource_id")
                    resource = resources.get(id=signing.loads(resource_id))
                    resource.name = name
                    resource.description = description
                    resource.price = price
                else:
                    resource = Resource(
                        name = name,
                        description = description,
                        price = price,
                        user = request.user
                    )
                resource.save()

            return redirect("groups_and_resources")
                
        return render(request, "main/groups_and_resources.html", context=context)

def another(request):
    return render(request, 'main/about.html', {"title": "About"})

def get_tasks(user, date):
    try:
        tasks = Task.objects.filter(user = user, date = date).order_by("is_completed", "priority")
    except:
        return None
    
    return tasks