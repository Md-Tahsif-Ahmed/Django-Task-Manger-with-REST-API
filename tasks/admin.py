from django.contrib import admin
from .models import Task, Photo

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'priority', 'is_complete', 'created_at', 'last_updated')
    list_filter = ('due_date', 'priority', 'is_complete')
    search_fields = ('title', 'description')

admin.site.register(Task, TaskAdmin)
admin.site.register(Photo)

 
