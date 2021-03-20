from django.db import models
from django.urls import reverse
from user.models import User
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from phonenumber_field.modelfields import PhoneNumberField

class StudentInternship(models.Model):
    startup = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=20)
    stipend = models.CharField(max_length=100)
    apply_by = models.DateField(default='2000-01-01', help_text='YYYY-MM-DD Format should be followed for the date.')
    link = models.URLField(default='', help_text='Add link for application. ')


    def __str__(self):
        return self.startup

    def get_absolute_url(self):
        return reverse('internship-detail', kwargs={'pk' : self.pk})


    def get_next_post(self):
        next_post = self.get_previous_by_apply_by()
        if next_post:
        	return next_post
        return False   	

    def get_prev_post(self):
        prev_post = self.get_next_by_apply_by()
        if prev_post:
        	return prev_post
        return False

class Project(models.Model):
    project = models.CharField(max_length=100, default='')
    field_of_project = models.CharField(max_length=100, default='')
    duration = models.CharField(max_length=20)
    about = models.TextField()
    location = models.CharField(max_length=100)
    stipend = models.CharField(max_length=100)
    skills_required = models.CharField(max_length=500)
    no_of_vaccancy = models.PositiveIntegerField()
    perks = models.CharField(max_length=100)
    apply_by = models.DateField(default='2000-01-01', help_text='YYYY-MM-DD Format should be followed for the date.')

    def __str__(self):
        return self.project

    def get_absolute_url(self):
        return reverse('internship-detail', kwargs={'pk' : self.pk})

    def about_markdown(self):
        about = self.about
        return mark_safe(markdown(about))

    def get_next_post(self):
        next_post = self.get_previous_by_apply_by()
        if next_post:
        	return next_post
        return False   	

    def get_prev_post(self):
        prev_post = self.get_next_by_apply_by()
        if prev_post:
        	return prev_post
        return False


class InternshipApplication(models.Model):
    internship = models.ForeignKey(Project, on_delete=models.CASCADE, default='', related_name='internship')
    message = models.TextField(max_length = 1200, blank=True, default='')
    resume = models.URLField(default='', help_text='Add the drive link to your resume.')
    applied_by = models.ForeignKey(User, on_delete=models.CASCADE, default='', related_name='intern')
    
    def __str__(self):
        return self.internship.startup.startup_name + "(" + str(self.internship.id) + ")" + " - " + self.applied_by.name

    def message_markdown(self):
        message = self.message
        return mark_safe(markdown(message))