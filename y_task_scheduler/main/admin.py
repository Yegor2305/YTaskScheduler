from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Task)
admin.site.register(Color)
admin.site.register(Group)
admin.site.register(Resource)
admin.site.register(TaskResources)