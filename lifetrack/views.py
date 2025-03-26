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
def add(p,f,v,m,F,V):
	att,err='',{}
	if p.get('form')=='add':
		el=f(p)
		if el.is_valid():
			att=el.cleaned_data['name']
			try:f.Meta.model.objects.get(name=att,**v)
			except f.Meta.model.DoesNotExist:
				e=el.save(commit=False);F(e,**V);e.save()
			else:err={'name':[m.format(att=att)]}
		else:err=dict(el.errors)
	return att,err
def al(l,u):l.user=u
def ah(h,l):h.list=l;h.sdate=adj[l.freq](h.sdate)
def edit(p,f,v,m,F,e,att):
	err={}
	if s:=p.get('form'):
		if s=='save':
			el=f(p)
			if el.is_valid():
				att=el.cleaned_data['name']
				try:
					f.Meta.model.objects.get(name=att,**v)
				except f.Meta.model.DoesNotExist:pass
				else:
					if e.name!=att:err={'name':[m.format(att=att)]}
				if not err:e.name=att;F(e,el.cleaned_data);e.save()
			else:err=dict(el.errors)
		elif s=='delete':
			e.delete()
	return att,err
def el(l,f):l.freq=f['freq']
def eh(h,d):h.sdate=adj[h.list.freq](d['sdate'])

def index(r):
	return render(r,'lifetrack/index.html')

def login(r):
	err={};status=200;uf=UserForm()
	if r.method=='POST':
		if r.POST.get('form')=='login':
			n=r.POST.get('username');p=r.POST.get('password')
			l=auth(username=n,password=p)
			if l:
				if l.is_active:li(r,l);return redirect(reverse('lifetrack:index'))
				else:status=401;err={'login':['Sorry, your account is disabled ☹︎ You must\'ve done something really wrong']}
			else:status=401;err={'login':['Bad username or password']}
		elif r.POST.get('form')=='signup':
			uf=UserForm(r.POST)
			if uf.is_valid():
				l=uf.save();l.set_password(l.password);l.save()
				err={'':['Thanks for registering!','Now try logging in ☺︎ (if it doesn\'t work someone\'s done something wrong — hopefully not us!)']}
			else:err=dict(uf.errors)
		else:err={'':['You\'ve done something very strange and sent us a request we don\'t understand']}
	return render(r,'lifetrack/login.html',context={'err':err},status=status)

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
	freq=''
	if r.method=='POST':freq=r.POST.get('freq')
	att,err=add(r.POST,ListForm,{'user':r.user},'You already have a habit list named {att}',al,{'u':r.user})
	if err or not r.POST.get('form'):return render(r,'lifetrack/addlist.html',context={'attempt':att,'freq':freq,'f':F,'err':err})
	else:return redirect(reverse('lifetrack:lists'))

def editlist(r):
	if r.method!='POST':return HttpResponse('How did you get here w/o POST; noöne\'ll know which list y\'want to edit!!1! URL Fishers get off my lawn',status=400)
	L=r.POST.get('ls')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('Somehow you\'ve supplied a nonexistent list. Not meant to be able to happen',status=404)
	freq=l.freq
	hb=Habit.objects.filter(list=l).order_by('name')
	if h:=r.POST.get('hb'):
		return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:edithabit')))
	att,err=edit(r.POST,ListForm,{'user':r.user},'You already have a habit list named {att}',el,l,L)
	if r.POST.get('form')=='addhabit':
		return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:addhabit')))
	if err or not r.POST.get('form'):
		return render(r,'lifetrack/editlist.html',context={'ls':L,'freq':freq,'hb':hb,'attempt':att,'err':err})
	else:return redirect(reverse('lifetrack:lists'))

def addhabit(r):
	if r.method!='POST':return HttpResponse('How did you get here w/o POST; noöne\'ll know which list y\'want to edit!!1! URL Fishers get off my lawn',status=400)
	L=r.POST.get('ls')
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('You\'nna try to add a habit to a a nonexistent list. Really?. I don\'t think so.',status=404)
	att,err=add(r.POST,HabitForm,{'list':l},'You already have a habit named {att}'+f' in the list {L}',ah,{'l':l})
	if err or r.POST.get('form')=='addhabit':return render(r,'lifetrack/addhabit.html',context={'ls':L,'attempt':att,'date':date.today().isoformat(),'err':err})
	else:return HttpResponsePassthruRedirect(resolve(reverse('lifetrack:editlist')))

def edithabit(r):
	if r.method!='POST':return HttpResponse('Begone URL Fishers getting here w/o POST; idk what habit to edit here',status=400)
	L,H=r.POST.get('ls'),r.POST.get('hb')
	att=H
	try:l=HabitList.objects.get(user=r.user,name=L)
	except HabitList.DoesNotExist:return HttpResponse('You\'nna try to change a habit in a nonexistent list. Yeah sure lol.',status=404)
	try:h=Habit.objects.get(name=H,list=l)
	except Habit.DoesNotExist:return HttpResponse('You\'nna try to change a nonexistent habit. Craaazy.',status=404)
	sdate=r.POST.get('sdate');sdate=sdate if sdate else h.sdate.isoformat()
	att,err=edit(r.POST,HabitForm,{'list':l},'You already have a habit list named {att}',eh,h,H)
	if err or not r.POST.get('form'):
		return render(r,'lifetrack/edithabit.html',context={'hb':h,'ls':l,'sdate':sdate,'attempt':att,'err':err})
	else:return redirect(reverse('lifetrack:lists'))

def log_out(r):
	logout(r)
	return redirect(reverse('lifetrack:index'))

def occur(r):
	if r.method!='POST':return HttpResponse(f'Stub. (occur)',status=400)
	s={'y':True,'n':False}[r.POST.get('set')]
	dt=date.fromisoformat(r.POST.get('dt'))
	try:hb=Habit.objects.get(list=HabitList.objects.get(user=r.user,name=r.POST.get('ls')),name=r.POST.get('hb'))
	except(HabitList.DoesNotExist,Habit.DoesNotExist):set=not s
	try:
		oc=Occurence.objects.get(date=dt,habit=hb);
		if not s:oc.delete();set=False
		else:set=True
	except Occurence.DoesNotExist:
		if s:oc=Occurence(date=dt,habit=hb);oc.save();set=True
		else:set=False
	return HttpResponse(f"{['n','y'][set]}")
