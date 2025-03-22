from django.shortcuts import render,redirect,resolve_url as resolve
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirectBase as RedirBase
from django.contrib.auth import authenticate as auth,login as li,logout
from lifetrack.models import *
from lifetrack.forms import *

F=['daily','weekly','monthly']
class HttpResponsePassthruRedirect(RedirBase):
    status_code=307

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
	return render(r,'lifetrack/addlist.html',context={'attempt':att,'f':F})

def editlist(r):
	if r.method!='POST':return HttpResponse('How did you get here w/o POST; noöne\'ll know which list y\'want to edit!!1! URL Fishers get off my lawn',status=400)
	L=r.POST.get('ls')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('Somehow you\'ve supplied a nonexistent list. Not meant to be able to happen',status=404)
	if f:=r.POST.get('form'):
		if f=='save':
			ls=ListForm(r.POST)
			if ls.is_valid():
				l.name,l.freq=ls.cleaned_data['name'],ls.cleaned_data['freq'];l.save()
				return redirect(reverse('lifetrack:lists'))
			else:print(ls.errors)
		elif f=='delete':
			l.delete();return redirect(reverse('lifetrack:lists'))
		elif f=='addhabit':
			l.delete();return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:addhabit')))
		else:freq=l.freq
	else:freq=l.freq
	return render(r,'lifetrack/editlist.html',context={'ls':L,'freq':freq,'f':F})

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
