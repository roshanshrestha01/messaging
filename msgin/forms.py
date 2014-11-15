from msgin.models import User, Group
from django import forms
from django.utils import timezone


class ComposeMessageForm(forms.Form):
    user_receivers = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'data-bind': 'selectize: {}, selectedOptions: selected_item',
                'placeholder': "Select User"}))
    group_receivers = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(
            attrs={
                'data-bind': 'selectize: {}, selectedOptions: selected_item1',
                'placeholder': "Select Group"}))
    message = forms.CharField(widget=forms.Textarea())
    schedule = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'data-bind': 'checked:tog, click:submit_save'}))
    scheduled_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(
            attrs={
                'data-bind': 'enable: tog'
            }))

    def clean(self):
        cleaned_data = super(ComposeMessageForm, self).clean()
        sch_time = cleaned_data.get("scheduled_time")
        if isinstance(sch_time, type(timezone.now())):
            if sch_time < timezone.now():
                msg = u"Message cannot be scheduled for past time !"
                self._errors["scheduled_time"] = self.error_class([msg])
                del cleaned_data["scheduled_time"]

        return cleaned_data
