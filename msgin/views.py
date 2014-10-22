from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from msgin.models import Message, User, Group
from django.utils import timezone
from django import forms
from msgin.tasks import scheduled_message
from msgin.celery import app
import re
from django.db.models import Q


class ComposeMessageForm(forms.Form):
    user_choice = User.objects.all().values_list('id', 'username')
    group_choice = Group.objects.all().values_list('id', 'name')
    user_receivers = forms.MultipleChoiceField(
        user_choice,
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'data-bind': 'selectedOptions: usr_receiver'}))
    group_receivers = forms.MultipleChoiceField(
        group_choice,
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'data-bind': 'selectedOptions: grp_receiver'}))
    message = forms.CharField(widget=forms.Textarea())
    schedule = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'data-bind': 'checked:tog, click:submit_save'}))
    scheduled_time = forms.DateTimeField(
        required=False)

    def clean(self):
        cleaned_data = super(ComposeMessageForm, self).clean()
        sch_time = cleaned_data.get("scheduled_time")
        if type(sch_time) == type(timezone.now()):
            if sch_time < timezone.now():
                msg = u"Message cannot be scheduled for past time !"
                self._errors["scheduled_time"] = self.error_class([msg])
                del cleaned_data["scheduled_time"]

        return cleaned_data


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
        new_message = Message.objects.get(id=msg_id)
        if new_message.status != 'OUTBOX':
            return HttpResponse("Only the outbox message is editable brother")
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
            else:
                stat = 'OUTBOX'
                scheduled = True

            if edit:
                app.control.revoke(get_task_id(msg_id), terminate=True)
                new_message.group_receiver.clear()
                new_message.user_receiver.clear()
            else:
                new_message = Message()

            new_message.sender = send_by
            new_message.message_content = message_c
            new_message.send_time = s_time
            new_message.status = stat
            new_message.created_at = timezone.now()
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
    group_name = request.user.groups.all()
    obj = Message.objects.filter(Q(user_receiver=request.user) | Q(
        group_receiver=group_name), status="SEND")
    return render(request, 'msgin/inbox.html', {'obj': obj})


def sent(request):
    obj = Message.objects.filter(sender=request.user, status="SEND")
    return render(request, "msgin/sent.html", {'obj': obj})


def outbox(request):
    obj = Message.objects.filter(sender=request.user, status="OUTBOX")
    return render(request, "msgin/outbox.html", {'obj': obj})


def messages_by_user(request, user_id):
    get_user = User.objects.get(id=user_id)
    obj = Message.objects.filter(
        sender=request.user,
        user_receiver=get_user,
        status="OUTBOX")
    return render(request, "msgin/outbox.html", {'obj': obj})


def messages_by_group(request, group_id):
    get_group = Group.objects.get(id=group_id)
    obj = Message.objects.filter(
        sender=request.user,
        group_receiver=get_group,
        status="OUTBOX")
    return render(request, "msgin/outbox.html", {'obj': obj})


def sent_msg_by_user(request, user_id):
    get_user = User.objects.get(id=user_id)
    obj = Message.objects.filter(
        sender=request.user,
        user_receiver=get_user,
        status="SEND")
    return render(request, "msgin/sent.html", {'obj': obj})


def sent_msg_by_group(request, group_id):
    get_group = Group.objects.get(id=group_id)
    obj = Message.objects.filter(
        sender=request.user,
        group_receiver=get_group,
        status="SEND")
    return render(request, "msgin/sent.html", {'obj': obj})
