from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.

@login_required
def all_subs(request):
	resources = Resource.objects.filter(resource_by=request.user)
	reminders = Reminder.objects.filter(reminder_by=request.user)
	context = {
		'resources' : resources,
		'reminders'	: reminders,
	}
	return render(request, 'resources/resource_home.html', context)