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


def all_slots(request):

	slots = Slot.objects.all()
	context = {
		'slots' : slots,
	}

	return render(request, 'booking/available_slots.html', context)

def time_sel(request, pk):

	slot = Slot.objects.get(id=pk)
	time = slot.time
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	print(time.first())
	print(slot)
	print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
