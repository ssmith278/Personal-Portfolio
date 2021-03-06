from django.db import models, transaction
from django.core.validators import RegexValidator
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.utils import timezone


# Create your models here.

# Abstract TimeStamped model
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ('-modified_at',)

# ContactInfo Model
#
#    Purpose:
#        A record of an applicant's contact information. Includes the following:
#
#        - Street Address (CharField):      Number and street name of applicant's residence
#        - City (CharField):                City of applicant's residence 
#        - State (CharField):               State of applicant's residence
#        - Zip Code (SmallIntegerField):    Zip code of applicant's residence    
#        - Phone Number (CharField):        Applicant's primary phone number (validated by regex)
#        - Email (EmailField):              Applicant's email address
#
class ContactInfo(TimeStamped):
    street_address = models.CharField(max_length=255, default='', help_text='Applicant\'s street address')
    city = models.CharField(max_length=64, default='', help_text='Applicant\'s city of residence')
    state = models.CharField(max_length=32, default='', help_text='Applicant\'s state of residence')
    zip_code = models.SmallIntegerField(default=00000, help_text='Applicant\'s zip code')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=10, help_text='10-digit contact phone number (assumed US number)')

    email = models.EmailField()

    def __str__(self):
        result = f'{self.created_at.date()} - {self.street_address}'

        return result

    def get_absolute_url(self):
        return reverse('contact-info-detail', args=[str(self.id)])

class Section(TimeStamped):
    section_title = models.CharField(max_length=255, default='', help_text='Title of this section (ie Experience, Organizations, etc.)')
    section_body = models.TextField(default='', help_text='Description bullets for the section')

    def __str__(self):
        result = f'{self.created_at.date()} - {self.section_title}\n'

        return result

    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.id)])

class Education(TimeStamped):
    school = models.CharField(max_length=255, default='', help_text='School attended')
    degree = models.CharField(max_length=255, default='', help_text='Degree obtained from education')
    graduation_date = models.CharField(max_length=32, default='', help_text='Date of graduation or expected graduation')
    gpa = models.FloatField(default=0.0, help_text='GPA received during degree')
    education_body = models.TextField(default='', help_text='Body of the section')

    def __str__(self):
        result = f'{self.school} {self.graduation_date}'
        return result

    def get_absolute_url(self):
        return reverse('education-detail', args=[str(self.id)])

class Employment(TimeStamped):
    company = models.CharField(max_length=255, default='', help_text='Company worked at during this employment')
    position = models.CharField(max_length=255, default='', help_text='Position while employed at the company')
    start_date = models.CharField(max_length=32, default='', help_text='Starting date at the given position')
    end_date = models.CharField(max_length=32, default='', help_text='Ending date of employment in the given position')
    employment_body = models.TextField(default='', help_text='Body of the section')

    def __str__(self):
        result = f'{self.company}, {self.position}'

        return result

    def get_absolute_url(self):
        return reverse('employment-detail', args=[str(self.id)])

#TODO: Add company/job applying for as a field to easily view/filter by 
class Resume(TimeStamped):
    full_name = models.CharField(max_length=255, default='', help_text='Full name of applicant')
    resume_date = models.DateField(default=timezone.now, help_text='Enter a date the resume was last applicable')
    contact_info = models.ForeignKey(ContactInfo, on_delete=SET_NULL, null=True)
    education_info = models.ManyToManyField(Education, related_name='+', help_text='Select education information about the applicant')
    employment_info = models.ManyToManyField(Employment, related_name='+', help_text='Select employment information about the applicant')
    other_sections = models.ManyToManyField(Section, related_name='+', help_text='Select any other sections to add to this resume')
    is_chosen = models.BooleanField(default=False, verbose_name='Active_Resume')

    class Meta:
        ordering = ('is_chosen', '-resume_date',)

    def save(self, *args, **kwargs):
        if not self.is_chosen:
            return super(Resume, self).save(*args, **kwargs)
        with transaction.atomic():
            Resume.objects.filter(
                is_chosen=True).update(is_chosen=False)
            return super(Resume, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.resume_date} - {self.full_name}\n'

    def get_absolute_url(self):
        return reverse('resume-detail', args=[str(self.id)])
