from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import ProjectInternshipForm
from .models import *
import datetime, xlwt
from django.db.models import Q
from django.core.paginator import Paginator


def InternshipProjects(request, pg=1):
    internships = Project.objects.all().order_by('-apply_by')
    context = {
        'internships': internships
    }
    return render(request, 'internshipPortal/ProjectInternship.html', context)

def Internships(request):
    internships = StudentInternship.objects.all().order_by('-apply_by')
    context = {
        'internships': internships
    }
    return render(request, 'internshipPortal/Internship.html', context)
    
    
def InternshipCreateView(request):
    pg = 1
    form = ProjectInternshipForm(request.POST or None)
    if request.user.is_authenticated and request.user.is_startup:
        if form.is_valid():
            form.instance.startup = request.user.startup_profile
            form.save()
            return redirect('internships', pg=pg)
    else:
        messages.success(request, f'You are not authorised to access this page.')
        return redirect('internships', pg=pg)

    context = {
        'form': form
    }
    return render(request, 'internshipPortal/create_internship.html', context)


def InternshipApplicationView(request, pk):
    internship = Internship.objects.filter(id=pk).first()
    applied_by = InternshipApplication.objects.filter(applied_by=request.user.student_profile)
    date = datetime.date.today()
    for applicant in applied_by:
        if(internship == applicant.internship):
            messages.success(request, f'You have already applied for that internship.')
            return redirect('internship-detail', pk)
    
    if(internship == None or date > internship.apply_by):
        messages.success(request, f'Applications for this internship closed.')
        return redirect('internships', pg = pg)
        

    form = ApplicationForm(request.POST or None)
    
    if form.is_valid():
        form.instance.internship = Internship.objects.filter(id = pk).first()
        form.instance.applied_by = request.user.student_profile
        form.save()
        return redirect('internship-detail', pk)

    context = {
        'form': form
    }
    return render(request, 'internshipPortal/application.html', context)



def InternshipDetailView(request, pk):
    pg = 1
    applied = False

    internship = Internship.objects.filter(id=pk).first()
    if(request.user.is_authenticated and request.user.is_student):
        applied_by = InternshipApplication.objects.filter(applied_by=request.user.student_profile)
        for applicant in applied_by:
            if(internship == applicant.internship):
                applied = True
    
    context = {
        'object' : internship,
        'applied' : applied,
    }

    return render(request, 'internshipPortal/internship_detail.html', context)


def InternshipUpdateView(request, pk):
    pg = 1
    if request.user.is_authenticated and request.user.is_startup and (request.user.startup_profile == Internship.objects.filter(id=pk).first().startup):
        if request.method == 'POST':
            form = ProjectInternshipForm(request.POST, instance=Internship.objects.filter(id=pk).first())
            
            if form.is_valid():
                form.save()
                return redirect('internships', pg=pg)

        form = ProjectInternshipForm(instance=Internship.objects.filter(id=pk).first())
        context = {
            'form': form
        }
        return render(request, 'internshipPortal/create_internship.html', context)

    else:
        messages.success(request, f'You are not authorised to access this page.')
        return redirect('internships', pg=pg)


def InternshipDeleteView(request, pk): 
    pg = 1
    obj = get_object_or_404(Internship, id=pk)
    internship = Internship.objects.filter(id=pk).first()
    if request.user.is_authenticated and request.user.is_startup and (request.user.startup_profile == obj.startup):
        if request.method =="POST":  
            obj.delete()  
            return redirect('internships', pg=pg)

    else:
        messages.success(request, f'You are not authorised to access this page')
        return redirect('internship-detail', pk)
    
    context ={
        'object' : internship
    }
  
    return render(request, 'internshipPortal/confirm_delete.html', context) 
