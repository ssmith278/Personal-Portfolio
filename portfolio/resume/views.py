from django.forms.models import model_to_dict
from django.shortcuts import render
from.models import Resume

# Create your views here.
def index(request):
    
    # Fetch information from db
    my_resume = Resume.objects.get(is_chosen=True)

    ## Information from resume

    # Form groups
    contact_info_dict = model_to_dict(my_resume.contact_info)
    education_dicts = list(my_resume.education_info.all())
    employment_dicts = list(my_resume.employment_info.all())
    other_sections_dicts = list(my_resume.other_sections.all())

    ## Details
    full_name = my_resume.full_name

    # Split bodies into bullets for custom formatting (this is so against DRY it hurts)
    for entry in education_dicts:
        entry.education_body = entry.education_body.splitlines()
        entry = model_to_dict(entry)

    for entry in employment_dicts:
        entry.employment_body = entry.employment_body.splitlines() 
        entry = model_to_dict(entry)

    for entry in other_sections_dicts:
        entry.section_body = entry.section_body.splitlines()
        entry = model_to_dict(entry)


    context = {
        'my_resume': my_resume,
        'full_name': full_name,
        'contact': contact_info_dict,
        'education': education_dicts,
        'employment': employment_dicts,
        'other': other_sections_dicts,
    }

    context.update(contact_info_dict)

    return render(request, 'index.html', context=context)
