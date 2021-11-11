from django.forms.models import model_to_dict
from django.shortcuts import render, get_object_or_404
from .models import Resume
from projects.models import Project

# Create your views here.
def index(request):
    
    # Fetch information from db
    my_resume = get_object_or_404(Resume, is_chosen=True)
    my_projects = Project.objects.all()

    # Resume information
    contact_info = my_resume.contact_info
    education = my_resume.education_info.all()
    employment = my_resume.employment_info.all()
    other_sections = my_resume.other_sections.all()

    # Projects

    ## Details
    full_name = my_resume.full_name
    
    context = {
        # Resume data
        'my_resume': my_resume,
        'full_name': full_name,
        'contact': contact_info,
        'education': education,
        'employment': employment,
        'other': other_sections,
        # Projects data
        'my_projects': my_projects,
    }

    return render(request, 'index.html', context=context)
