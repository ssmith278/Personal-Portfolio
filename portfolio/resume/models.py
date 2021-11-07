from django.db import models
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

#TODO: Change body field in sections/education/employment to a ForeignKey(OneToMany) of CharFields
class ContactInfo(TimeStamped):
    street_address = models.CharField(max_length=255, help_text='Applicant\'s street address')
    city = models.CharField(max_length=64, help_text='Applicant\'s city of residence')
    state = models.CharField(max_length=32, help_text='Applicant\'s state of residence')
    zip_code = models.SmallIntegerField(help_text='Applicant\'s zip code')

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=10, help_text='10-digit contact phone number (assumed US number)')

    email = models.EmailField()

    def __str__(self):
        result = f'{self.created_at.date()} - {self.street_address}'

        return result

    def get_absolute_url(self):
        return reverse('contact-info-detail', args=[str(self.id)])

class Section(TimeStamped):
    section_title = models.CharField(max_length=255, help_text='Title of this section (ie Experience, Organizations, etc.)')
    section_body = models.TextField(default='', help_text='Body of the section')

    def __str__(self):
        result = f'{self.created_at.date()} - {self.section_title}\n'

        return result

    def get_absolute_url(self):
        return reverse('section-detail', args=[str(self.id)])

class Education(TimeStamped):
    school = models.CharField(max_length=255, help_text='School attended')
    degree = models.CharField(max_length=255, help_text='Degree obtained from education')
    gpa = models.FloatField(help_text='GPA received during degree')
    education_body = models.TextField(default='',help_text='Body of the section')

    def __str__(self):
        result = f'{self.created_at.date()} - {self.school}'
        return result

    def get_absolute_url(self):
        return reverse('education-detail', args=[str(self.id)])

class Employment(TimeStamped):
    company = models.CharField(max_length=255, help_text='Company worked at during this employment')
    position = models.CharField(max_length=255, help_text='Position while employed at the company')
    employment_body = models.TextField(default='', help_text='Body of the section')

    def __str__(self):
        result = f'{self.created_at.date()} - {self.company}, {self.position}'

        return result

    def get_absolute_url(self):
        return reverse('employment-detail', args=[str(self.id)])

#TODO: Add company/job applying for as a field to easily view/filter by 
class Resume(TimeStamped):
    full_name = models.CharField(max_length=255, help_text='Full name of applicant')
    resume_date = models.DateField(help_text='Enter a date the resume was last applicable')
    contact_info = models.ForeignKey(ContactInfo, on_delete=SET_NULL, null=True)
    education_info = models.ManyToManyField(Education, related_name='+', help_text='Select education information about the applicant')
    employment_info = models.ManyToManyField(Employment, related_name='+', help_text='Select employment information about the applicant')
    other_sections = models.ManyToManyField(Section, related_name='+', help_text='Select any other sections to add to this resume')

    class Meta:
        ordering = ('-resume_date',)

    def __str__(self):
        return f'{self.resume_date} - {self.full_name}\n'

    def get_absolute_url(self):
        return reverse('resume-detail', args=[str(self.id)])