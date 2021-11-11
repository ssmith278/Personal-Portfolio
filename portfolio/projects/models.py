from django.db import models
from django.urls import reverse
from django.utils import timezone

# Create your models here.

# Abstract TimeStamped model
class TimeStamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(TimeStamped):
    title = models.CharField(max_length=64)
    start_date = models.DateField(default=timezone.now, help_text='Date of project start')
    end_date = models.DateField(default=None, blank=True, null=True, help_text='Date of project completion')
    languages = models.CharField(default='', max_length=256, help_text='Languages used when developing this project')
    technologies = models.CharField(default='', max_length=256, help_text='Technologies used when developing this project')
    description = models.CharField(default='', max_length=256, help_text='Short description of project')
    github_page = models.URLField(default=None, blank=True, null=True, max_length=256, help_text='Link to the project\'s GitHub page.')

    class Meta:
        ordering = ('title', '-start_date')

    def __str__(self):
        result = f'{self.title} ({self.start_date.year})'

        return result

    def get_absolute_url(self):
        return reverse('project-detail', args=[str(self.id)])