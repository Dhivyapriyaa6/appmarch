from django.contrib import admin
from .models import Activity, ActivityPhoto

class PhotoInline(admin.TabularInline):
    model = ActivityPhoto
    extra = 1

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['team_name', 'date', 'members', 'created_at']
    inlines = [PhotoInline]
