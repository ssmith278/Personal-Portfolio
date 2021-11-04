from django.contrib import admin
from .models import ContactInfo, Section, Education, Employment, Resume

# Register your models here.
admin.site.register(ContactInfo)
admin.site.register(Section)
admin.site.register(Education)
admin.site.register(Employment)
admin.site.register(Resume)
