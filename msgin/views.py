from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from msgin.models import Message, User, Group
from django.utils import timezone
from django import forms
from msgin.tasks import scheduled_message
from msgin.celery import app
import re


class ComposeMessageForm(forms.Form):
    user_choice = User.objects.all().values_list('id', 'username')
    group_choice = Group.objects.all().values_list('id', 'name')
    user_receivers = forms.MultipleChoiceField(user_choice, required=False)
    group_receivers = forms.MultipleChoiceField(group_choice, required=False)
    message = forms.CharField(widget=forms.Textarea())
    schedule = forms.BooleanField(required=False)
    scheduled_time = forms.DateTimeField(
        required=False,
        widget=forms.SplitDateTimeWidget())


def get_related_list(obj):
    l = []
    for o in obj:
        l.append(o.id)
    return l


def get_waiting_time_sec(time_obj):
    current_tz = timezone.get_current_timezone()
    current_time = timezone.now()
    current_tz_time = current_time.astimezone(current_tz)
    waiting_time = time_obj - current_tz_time
    return waiting_time.seconds


def get_task_id(ms_id):
    i = app.control.inspect()
    sch_ms = i.scheduled()
    sch_ms_list = sch_ms['celery@localhost.localdomain']
    for l in range(len(sch_ms_list)):
        smt = sch_ms_list[l]['request']['args']
        if int(ms_id) == int(re.findall(r'\d*\w', smt)[0]):
            task_id = sch_ms_list[l]['request']['id']
    return task_id


def index(request):
    return render(request, 'msgin/index.html')


def compose(request, msg_id=None):
    if msg_id is not None:
        edit = True
    else:
        edit = False
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            scheduled = False
            send_by = request.user
            u_receiver = form.cleaned_data['user_receivers']
            g_receiver = form.cleaned_data['group_receivers']
            message_c = form.cleaned_data['message']
            s_time = form.cleaned_data['scheduled_time']
            if s_time is None:
                stat = 'SEND'
                # Delete here the task while edit
            else:
                stat = 'OUTBOX'
                scheduled = True

            if edit:
                app.control.revoke(get_task_id(msg_id), terminate=True)
                new_message = Message.objects.get(id=msg_id)
                new_message.group_receiver.clear()
                new_message.user_receiver.clear()
            else:
                new_message = Message()

            new_message.sender = send_by
            new_message.message_content = message_c
            new_message.send_time = s_time
            new_message.status = stat
            new_message.save()
            new_message.group_receiver.add(*g_receiver)
            new_message.user_receiver.add(*u_receiver)
            if scheduled:
                message_id = new_message.id
                scheduled_message.apply_async(
                    (message_id,), countdown=get_waiting_time_sec(
                        new_message.send_time))
            return HttpResponseRedirect('/message/')
    else:
        if edit:
            e_message = Message.objects.get(id=msg_id)
            data = {'user_receivers': get_related_list(
                        e_message.user_receiver.all()),
                    'group_receivers': get_related_list(
                        e_message.group_receiver.all()),
                    'message': e_message.message_content,
                    'scheduled_time': e_message.send_time,
                    }
            form = ComposeMessageForm(data)
        else:
            form = ComposeMessageForm()
    context = {'form': form, 'message_id': msg_id}
    return render(request, 'msgin/compose_message.html', context)


def inbox(request):

    return HttpResponse('This is inbox bro')


def send(request):
    pass


def outbox(request):
    pass
