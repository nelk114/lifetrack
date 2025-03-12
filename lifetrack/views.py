from django.shortcuts import render
from django.http import HttpResponse

def index(r):
	return render(r,'lifetrack/index.html')

def login(r):
	return HttpResponse(f'Stub. (login)')

def lists(r):
	return HttpResponse(f'Stub. (lists)')

def addlist(r):
	return HttpResponse(f'Stub. (addlist)')

def editlist(r):
	return HttpResponse(f'Stub. (editlist)')

def addhabit(r):
	return HttpResponse(f'Stub. (addhabit)')

def edithabit(r):
	return HttpResponse(f'Stub. (edithabit)')


