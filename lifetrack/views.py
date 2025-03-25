from django.shortcuts import render,redirect,resolve_url as resolve
from django.urls import reverse
from django.http import HttpResponse
from django.http.response import HttpResponseRedirectBase as RedirBase
from django.contrib.auth import authenticate as auth,login as li,logout
from lifetrack.models import *
from lifetrack.forms import *
from datetime import date,timedelta as Δt

F=['daily','weekly','monthly']
WD=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
RD=['Yesterday','Today']
RW=['Last Week','This Week']
MÞ=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
RM=['Last Month','This Month']
adj={'daily':lambda x:x,'weekly':lambda x:x-Δt(days=x.weekday()),'monthly':lambda x:x.replace(day=1)}
maxnr={'daily':7,'weekly':8,'monthly':10}
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
	dt=date.today()
	dy=[dt-Δt(days=i)for i in range(maxnr['daily'])][::-1]
	dyn=[WD[d.weekday()]for d in dy][:-len(RD)]+RD
	wt=adj['weekly'](dt);wk=[wt-Δt(days=i*7)for i in range(maxnr['weekly'])][::-1];wkn=[f'W/b {d.day}/{d.month}'for d in wk][:-len(RW)]+RW
	mt=adj['monthly'](dt);mþ=[mt];
	for i in range(maxnr['monthly']-1):mþ.append(mt:=(mt-Δt(days=1)).replace(day=1))
	mþ=mþ[::-1];mþn=[MÞ[d.month-1]for d in mþ][:-len(RM)]+RM
	lss=[]
	ls=HabitList.objects.filter(user=r.user).order_by('name')
	for l in ls:
		c={'l':l};hb=Habit.objects.filter(list=l).order_by('name')
		if hb:
			lh=[]
			sd=min([h.sdate for h in hb])
			ld=[d for d in zip(*{'daily':(dy,dyn),'weekly':(wk,wkn),'monthly':(mþ,mþn)}[l.freq])if d[0]>=sd]
			for h in Habit.objects.filter(list=l).order_by('name'):
				hc={'h':h,'o':[(d[0].isoformat(),Occurence.objects.filter(date=d[0],habit=h).exists(),d[0]>=h.sdate)for d in ld]};lh.append(hc)
			c['h']=lh;c['d']=[d[1]for d in ld];
		lss.append(c)
	return render(r,'lifetrack/lists.html',context={'ls':lss})

def addlist(r):
	att,freq='',''
	if r.method=='POST' and r.POST.get('form'):
		freq=r.POST.get('freq')
		ls=ListForm(r.POST)
		if ls.is_valid():
			att=ls.cleaned_data['name']
			try:
				HabitList.objects.get(user=r.user,name=att)
			except HabitList.DoesNotExist:
				l=ls.save(commit=False);l.user=r.user;l.save()
				return redirect(reverse('lifetrack:lists'))
		else:print(ls.errors)
	return render(r,'lifetrack/addlist.html',context={'attempt':att,'freq':freq,'f':F})

def editlist(r):
	if r.method!='POST':return HttpResponse('How did you get here w/o POST; noöne\'ll know which list y\'want to edit!!1! URL Fishers get off my lawn',status=400)
	L=r.POST.get('ls')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('Somehow you\'ve supplied a nonexistent list. Not meant to be able to happen',status=404)
	hb=Habit.objects.filter(list=l).order_by('name')
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
			return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:addhabit')))
		else:freq=l.freq
	elif h:=r.POST.get('hb'):
		return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:edithabit')))
	else:freq=l.freq
	return render(r,'lifetrack/editlist.html',context={'ls':L,'freq':freq,'hb':hb})

def addhabit(r):
	if r.method!='POST':return HttpResponse('How did you get here w/o POST; noöne\'ll know which list y\'want to edit!!1! URL Fishers get off my lawn',status=400)
	att=''
	L=r.POST.get('ls')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('You\'nna try to add a habit to a a nonexistent list. Really?. I don\'t think so.',status=404)
	if r.POST.get('form')=='add':
		hb=HabitForm(r.POST)
		if hb.is_valid():
			att=hb.cleaned_data['name']
			try:
				Habit.objects.get(name=att,list=l)
			except Habit.DoesNotExist:
				h=hb.save(commit=False);h.list=l;h.sdate=adj[l.freq](h.sdate);h.save()
				return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:editlist')))
		else:print(hb.errors)
	return render(r,'lifetrack/addhabit.html',context={'ls':L,'attempt':att,'date':date.today().isoformat()})

def edithabit(r):
	if r.method!='POST':return HttpResponse('Begone URL Fishers getting here w/o POST; idk what habit to edit here',status=400)
	L,H=r.POST.get('ls'),r.POST.get('hb')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('You\'nna try to change a habit in a nonexistent list. Yeah sure lol.',status=404)
	try:h=Habit.objects.get(name=H,list=l)
	except Habit.DoesNotExist:return HttpResponse('You\'nna try to change a nonexistent habit. Craaazy.',status=404)
	if f:=r.POST.get('form'):
		if f=='save':
			hb=HabitForm(r.POST)
			if hb.is_valid():
				h.name,h.sdate=hb.cleaned_data['name'],adj[l.freq](hb.cleaned_data['sdate']);h.save()
				return redirect(reverse('lifetrack:lists'))
			else:print(hb.errors)
		elif f=='delete':
			h.delete();return redirect(reverse('lifetrack:lists'))
		else:freq=l.freq
	else:freq=l.freq
	return render(r,'lifetrack/edithabit.html',context={'hb':h,'ls':l})

def log_out(r):
	logout(r)
	return redirect(reverse('lifetrack:index'))

def occur(r):
	if r.method!='POST':return HttpResponse(f'Stub. (occur)',status=400)
	[print(o,r.POST.get(o))for o in r.POST]
	s={'y':True,'n':False}[r.POST.get('set')]
	dt=date.fromisoformat(r.POST.get('dt'))
	try:hb=Habit.objects.get(list=HabitList.objects.get(user=r.user,name=r.POST.get('ls')),name=r.POST.get('hb'))
	except(HabitList.DoesNotExist,Habit.DoesNotExist):print(1235);set=not s
	try:
		oc=Occurence.objects.get(date=dt,habit=hb);
		if not s:oc.delete();set=False;print('del\t',oc)
		else:set=True;print('ext\t',oc)
	except Occurence.DoesNotExist:
		if s:oc=Occurence(date=dt,habit=hb);oc.save();set=True;print('reg\t',oc)
		else:set=False;print('non\t',oc)
	[print(o)for o in Occurence.objects.filter(habit=hb)]
	return HttpResponse(f"{['n','y'][set]}")
