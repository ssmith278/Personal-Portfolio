from django.shortcuts import render
from.models import Resume

# Create your views here.
def index(request):
    
    # Fetch information from db
    my_resume = Resume.objects.first()

    ## Information from resume

    # Form groups
    contact_info_dict = vars(my_resume.contact_info)
    education_info = list(my_resume.education_info.all())
    employment_info = my_resume.employment_info
    other_sections = my_resume.other_sections

    ## Details
    full_name = my_resume.full_name

    


    context = {
        'my_resume': my_resume,
        'full_name': full_name,
    }

    context.update(contact_info_dict)
    context.update(vars(education_info[0]))

    return render(request, 'index.html', context=context)
