from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import InternshipForm, ApplicationForm
from .models import Internship, InternshipApplication, VentureCapitalist
import datetime, xlwt
from django.db.models import Q
from django.core.paginator import Paginator


def Internships(request, pg=1):
    internship = Internship.objects.all().order_by('-apply_by')

    query = request.GET.get("query")
    if query:
        internship = internship.filter(
            # Q(startup__icontains=query) |
            Q(field_of_internship__icontains=query) |
            Q(duration__icontains=query) |
            Q(about=query) |
            Q(location=query) |
            Q(stipend=query) |
            Q(skills_required=query) |
            Q(perks=query) 
            ).distinct()

    paginator = Paginator(internship, 8)

    context = {
        'Intern': paginator.page(pg),
        'page': pg,
      	'paginator': paginator,
        'internships': paginator.page(pg)
    }
    return render(request, 'internshipPortal/Internship.html', context)

def MyInternships(request):
    pg = 1
    if(request.user.is_authenticated and request.user.is_startup):
        internships = Internship.objects.filter(startup=request.user.startup_profile).order_by('-apply_by')
        context = {
            'internships': internships,
        }
        return render(request, 'internshipPortal/MyInternshipStartup.html', context)
    elif(request.user.is_authenticated and request.user.is_student):
        internships = InternshipApplication.objects.filter(applied_by=request.user.student_profile)
        context = {
            'internships': internships,
        }
        return render(request, 'internshipPortal/MyInternshipStudent.html', context)
    else:
        redirect(internships, pg=pg)
    
    

def InternshipCreateView(request):
    pg = 1
    form = InternshipForm(request.POST or None)
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
    pg = 1
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
            form = InternshipForm(request.POST, instance=Internship.objects.filter(id=pk).first())
            
            if form.is_valid():
                form.save()
                return redirect('internships', pg=pg)

        form = InternshipForm(instance=Internship.objects.filter(id=pk).first())
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
