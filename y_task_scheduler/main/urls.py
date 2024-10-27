from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('tasks/', views.tasks_page, name="tasks"),
    path('groups_and_resources/', views.groups_and_resources_page, name="groups_and_resources"),
    path('log-out', views.log_out, name="log-out"),
    path('about', views.another, name="about"),
]