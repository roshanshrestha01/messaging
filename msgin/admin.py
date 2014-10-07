from django.contrib import admin
from msgin.models import Message


class ViewChange(admin.ModelAdmin):

    list_display = ['sender', 'message_content', 'status']
    list_filter = ['status']

admin.site.register(Message, ViewChange)

# Register your models here.
