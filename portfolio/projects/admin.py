from django.contrib import admin
from .models import Project

# Register your models here.
@admin.register(Project)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'languages', 'github_page')
    list_filter = ('start_date', 'end_date', 'languages', 'technologies')