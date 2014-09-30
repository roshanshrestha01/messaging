from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from msgin.models import Message
from django.utils import timezone
from django import forms
from django.forms import ModelForm
from msgin.tasks import scheduled_message
import pdb

class ComposeMessageForm(forms.ModelForm):
	class Meta:
		model = Message
		exclude = ['sender','status']
		widgets = {
			'send_time':forms.SplitDateTimeWidget,
		}


def index(request):
	return render(request,'msgin/index.html')
	#return HttpResponse('Here will be compose and inbox')

def compose(request):
	if request.method == 'POST':
		form = ComposeMessageForm(request.POST)
		#if form.is_valid() and form.cleaned_data['send_time'] = None:
		if form.is_valid():
			scheduled = False
			send_status = form.save(commit = False)
			send_status.sender = request.user
			if form.cleaned_data['send_time'] == None:
				send_status.status = 'SEND'
			else:
				send_status.status = 'OUTBOX'
				scheduled=True
			send_status.save()
			form.save_m2m()
			if scheduled:
				message_id = send_status.id
				current_tz = timezone.get_current_timezone()
				current_time = timezone.now()
				current_tz_time = current_time.astimezone(current_tz)
				waiting_time = send_status.send_time - current_tz_time
				waiting_time_in_seconds = waiting_time.seconds
				scheduled_message.delay(message_id,waiting_time_in_seconds)
				#scheduled_message.apply_async((message_id,),queue='lopri', countdown=waiting_time_in_seconds)
				#pdb.set_trace()
				

			return HttpResponseRedirect('/message/')
		'''else:
			form.save(commit=False)'''

	else:
		form = ComposeMessageForm()
		context = {'form':form}
		return render(request,'msgin/compose_message.html',context)

def inbox(request):
	pass

def send(request):
	pass

def outbox(request):
	pass
# Create your views here.
