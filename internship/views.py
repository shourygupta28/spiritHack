from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from .forms import ProjectInternshipForm, InternshipForm, ApplicationForm
from .models import *
import datetime, xlwt
from django.db.models import Q
from django.core.paginator import Paginator


def InternshipProjects(request):
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
    if request.method == 'POST':
        if request.user.is_student:
            form = InternshipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Your submission has been sent to our team for review.')
        else:
            form = ProjectInternshipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(
                    request, 'Done!')

        return HttpResponseRedirect(reverse('internships'))

    else:
        if request.user.is_student:
            form = InternshipForm(request.POST, request.FILES)
        else:
            form = ProjectInternshipForm(request.POST, request.FILES)

    context = {
        'form': form,
    }

    return render(request, 'internship/CreateInternship.html', context)

def apply(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Done!')
            return HttpResponseRedirect(reverse('internships'))

    else:
        form = ApplicationForm(request.POST, request.FILES)

    context = {
        'form': form,
    }

    return render(request, 'internship/ApplyforInternship.html', context)



