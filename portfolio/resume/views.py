from django.core.mail import mail_admins, message
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
import sys
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

    # Contact Post
    if request.method == 'POST':
        message_sent(request)

    return render(request, 'index.html', context=context)

def message_sent(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        description = request.POST.get('description', None)

        if name and email and description:
            try:
                mail_admins(
                    subject='Contact Form (from %s)'%': '.join([name,email]),
                    message=description,
                    )
                # Send user to success page then redirect back
                return HttpResponseRedirect('')
            except Exception as e:
                print('Failed to send admin email\n%s'%e, file=sys.stderr)

    return JsonResponse({
        'message_sent_success': request.session.get('message_sent_success', False)
    })
