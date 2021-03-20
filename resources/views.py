from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def all_subs(request):
	resources = Resource.objects.filter(resource_by=request.user)
	reminders = Reminder.objects.filter(reminder_by=request.user)
	# subjects = Subject.objects.filter(yr_branch=request.user.yr_branch)
	subjects = Subject.objects.filter()
	context = {
		'resources' : resources,
		'reminders'	: reminders,
		'subjects' : subjects,
	}
	return render(request, 'resources/resource_home.html', context)

def create_resource(request):
	if(request.method == 'POST'):
		form = ResourceForm(request.POST, request.FILES)
		if form.is_valid():
			form.instance.resource_by = request.user
			form.instance.resource_by = request.user
			form.save()
	
	form = ResourceForm()
	context = {
		'form' : form,
	}
	return render(request, 'resources/resource_form.html', context)

def delete_resource(request, pk):
	resource = Resource.objects.get(id=pk)
	if(request.user == Resource.resource_by):
		resources.delete()
	else:
			messages.add_message(request, messages.INFO, 'You are not authorized to delete this feed.')

	return redirect('resources')


def delete_reminder(request, pk):
	reminder = Reminder.objects.get(id=pk)
	if(request.user == reminder.reminder_by):
		reminder.delete()
	else:
			messages.add_message(request, messages.INFO, 'You are not authorized to delete this feed.')

	return redirect('resources')

def subject_page(request, id):
	subject = Subject.objects.get(id=id)
	resources = Resource.objects.filter(resource_by=request.user, Subject=subject)
	reminders = Reminder.objects.filter(resource_by=request.user, Subject=subject)

	context = {
		'resources' : resources,
		'reminders'	: reminders,
		'subject' : subject,
	}
	return render(request, 'resources/subject_page.html', context)