from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *

# Create your views here.
@login_required
def create_slot(request):
	if(request.user.is_teacher == True):
		if(request.method == 'POST'):
			form = SlotForm(request.POST)
			if form.is_valid():
				form.instance.teacher = request.user
				form.save()
			return redirect('slots')
		form = SlotForm()
		context = {
			'form' : form,
		}
		return render(request, 'booking/slot_form.html', context)
	else:
		return redirect('slots')


def all_slots(request, pk=None, id=None):

	slots = Slot.objects.all()
	if id:
		slot = Slot.objects.get(id=pk)
		time_slot = Time.objects.get(id=id)
		timeName = time_slot.time
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
		print(timeName)
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
		form = SlotForm()
		form.instance.stundent = request.user
		form.instance.teacher = slot.teacher
		form.instance.time.set(time_slot.first())
		form.instance.date = slot.date
		form.save()
	
	context = {
		'slots' : slots,
	}

	return render(request, 'booking/available_slots.html', context)

# def time_sel(request, pk):

# 	slot = Slot.objects.get(id=pk)
# 	times = slot.time
# 	if(request.method == 'POST'):
# 		form = SlotForm(request.POST)
# 		if form.is_valid():
# 			form.instance.stundent = request.user
# 			form.instance.teacher = slot.teacher
# 			form.instance.time = time.time
# 			form.instance.date = slot.date

# 			form.save()
# 			return redirect('slots')

# 	context = {
# 		'times' : times,
# 		'slot' : slot,
# 	}
# 	return render(request, 'booking/available_time.html', context)
