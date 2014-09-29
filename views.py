from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
	return HttpResponse('This is the homepage')