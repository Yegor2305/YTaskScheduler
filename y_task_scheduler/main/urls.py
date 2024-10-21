from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('tasks/', views.personal_page, name="tasks"),
    path('log-out', views.log_out, name="log-out"),
    path('about', views.another, name="about"),
]