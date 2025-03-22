from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate as auth,login as li,logout
from lifetrack.models import *
from lifetrack.forms import *

def index(r):
	return render(r,'lifetrack/index.html')

def login(r):
	reg,fail=False,False;status=200;uf=UserForm()
	if r.method=='POST':
		if r.POST.get('form')=='login':
			n=r.POST.get('username');p=r.POST.get('password')
			l=auth(username=n,password=p)
			if l:
				if l.is_active:li(r,l);return redirect(reverse('lifetrack:index'))
				else:print(f'Disabled account: {n}');fail,status='disabled',401
			else:print(f'Invalid login details: {n}, {p}');fail,status='login',401
		elif r.POST.get('form')=='signup':
			uf=UserForm(r.POST)
			if uf.is_valid():
				l=uf.save();l.set_password(l.password);l.save()
				reg=True
			else:print(uf.errors,pf.errors)
		else:print('Unsupported form submission')
	return render(r,'lifetrack/login.html',context={'user_form':uf,'registered':reg,'fail':fail},status=status)

def lists(r):
	ls=HabitList.objects.order_by('name')
	return render(r,'lifetrack/lists.html',context={'ls':ls})

def addlist(r):
	att=None
	if r.method=='POST' and r.POST.get('form'):
		ls=ListForm(r.POST)
		if ls.is_valid():
			att=ls.cleaned_data['name']
			try:
				HabitList.objects.get(user=r.user,name=att)
			except HabitList.DoesNotExist:
				l=ls.save(commit=False);l.user=r.user;l.save()
				return redirect(reverse('lifetrack:lists'))
		else:print(ls.errors)
	return render(r,'lifetrack/addlist.html',context={'attempt':att})

def editlist(r):
	return render(r,'lifetrack/editlist.html',context={'ls':ls})

def addhabit(r):
	return render(r,'lifetrack/addhabit.html')

def edithabit(r):
	return render(r,'lifetrack/edithabit.html')

def log_out(r):
	logout(r)
	return redirect(reverse('lifetrack:index'))

def occur(r):
	if r.method=='POST':
		return HttpResponse(f"Stub. (occur)\n{r.POST.get('dt')}\n{r.POST.get('hb')}\n{r.POST.get('ls')}")
	return HttpResponse(f'Stub. (occur)',status=400)
