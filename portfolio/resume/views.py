from django.shortcuts import render
from.models import Resume

# Create your views here.
def index(request):
    
    # Fetch information from db
    my_resume = Resume.objects.first()

    # Get information from resume

    # From groups
    contact_info = my_resume.contact_info
    education_info = my_resume.education_info
    employment_info = my_resume.employment_info
    other_sections = my_resume.other_sections

    # Details
    full_name = my_resume.full_name
    phone_number = contact_info.phone_number


    context = {
        'my_resume': my_resume,
        'full_name': full_name,
        'phone_number': phone_number,
    }

    return render(request, 'index.html', context=context)
