from django.contrib import admin
from .models import Project, SavedProject


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'client', 'category', 'status', 'budget_min', 'budget_max', 'deadline', 'created_at')
    list_filter = ('status', 'category', 'level', 'budget_type')
    search_fields = ('title', 'description', 'client__username')
    date_hierarchy = 'created_at'


@admin.register(SavedProject)
class SavedProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project', 'created_at')
    search_fields = ('user__username', 'project__title')
