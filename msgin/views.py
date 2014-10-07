from django.shortcuts import render
from django.http import HttpResponseRedirect
from msgin.models import Message, User, Group
from django.utils import timezone
from django import forms
# from django.forms import ModelForm
from msgin.tasks import scheduled_message
from django.db.models import Q
import datetime


class ComposeMessageForm(forms.Form):
    user_choice = User.objects.all().values_list('id', 'username')
    group_choice = Group.objects.all().values_list('id', 'name')
    user_receivers = forms.MultipleChoiceField(user_choice, required=False)
    group_receivers = forms.MultipleChoiceField(group_choice, required=False)
    message = forms.CharField(widget=forms.Textarea())
    schedule = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'data-bind': 'checked:tog, click:submit_save'}))
    scheduled_time = forms.DateTimeField(
        required=False,
        widget=forms.SplitDateTimeWidget())


def index(request):
    return render(request, 'msgin/index.html')
    # return HttpResponse('Here will be compose and inbox')


def compose(request):
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        # if form.is_valid() and form.cleaned_data['send_time'] = None:
        if form.is_valid():
            scheduled = False
            send_by = request.user
            u_receiver = form.cleaned_data['user_receivers']
            g_receiver = form.cleaned_data['group_receivers']
            message_c = form.cleaned_data['message']
            s_time = form.cleaned_data['scheduled_time']
            create_at = datetime.date.today()
            if s_time is None:
                stat = 'SEND'
            else:
                stat = 'OUTBOX'
                scheduled = True
            new_message = Message(
                sender=send_by,
                message_content=message_c,
                send_time=s_time,
                status=stat,
                created_at=create_at)
            new_message.save()
            # pdb.set_trace()
            new_message.group_receiver.add(*g_receiver)
            new_message.user_receiver.add(*u_receiver)
            if scheduled:
                message_id = new_message.id
                current_tz = timezone.get_current_timezone()
                current_time = timezone.now()
                current_tz_time = current_time.astimezone(current_tz)
                waiting_time = new_message.send_time - current_tz_time
                waiting_time_in_seconds = waiting_time.seconds
                scheduled_message.delay(message_id, waiting_time_in_seconds)
            return HttpResponseRedirect('/message/')
    else:
        form = ComposeMessageForm()
    context = {'form': form}
    return render(request, 'msgin/compose_message.html', context)


def inbox(request):
    group_name = request.user.groups.all()
    obj = Message.objects.filter(Q(user_receiver=request.user) | Q(
        group_receiver=group_name), status="SEND").order_by('-created_at')
    return render(request, 'msgin/inbox.html', {'obj': obj})


def send(request):
    pass


def outbox(request):
    obj = Message.objects.filter(sender=request.user, status="OUTBOX")
    return render(request, "msgin/outbox.html", {'obj': obj})
# Create your views here.
