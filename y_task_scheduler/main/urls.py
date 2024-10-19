from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('account', views.personal_page, name="account"),
    path('log-out', views.log_out, name="log-out"),
    path('about', views.another, name="about")
]