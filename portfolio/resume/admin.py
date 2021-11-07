from django.contrib import admin
from .models import ContactInfo, Section, Education, Employment, Resume

# Register your models here.
#admin.site.register(ContactInfo)
#admin.site.register(Section)
#admin.site.register(Education)
#admin.site.register(Employment)
#admin.site.register(Resume)

#Extends default admin behavior to define model-specific admin behavior
#TODO: Add list views for all models
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('modified_at', 'city', 'state', 'phone_number', 'email')
    list_filter = ('modified_at', 'city', 'state')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('modified_at', 'section_title')
    list_filter = ('modified_at', 'section_title')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('modified_at', 'school', 'degree', 'gpa')
    list_filter = ('modified_at', 'school')

@admin.register(Employment)
class EmploymentAdmin(admin.ModelAdmin):
    list_display = ('modified_at', 'company')
    list_filter = ('modified_at', 'company')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('resume_date', 'modified_at', 'full_name')
    list_filter = ('resume_date', 'modified_at', 'full_name')
