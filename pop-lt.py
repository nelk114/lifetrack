import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','lt.settings')
import django
django.setup()
from lifetrack.models import *
from lifetrack.forms import UserForm
from lifetrack.views import adj
from datetime import date,timedelta as Δt

def dateback(Δ):
	return date.today()-Δt(days=Δ)
def addusr(n,p,N):
	uf=UserForm({'username':n,'password':p,'first_name':n})
	u=uf.save();u.set_password(u.password);u.save()
	return u
def addls(u,n,f):
	ls=HabitList.objects.get_or_create(user=u,name=n)[0]
	ls.freq=f;ls.save()
	return ls
def addhb(l,n,d,oc):
	hb=Habit.objects.get_or_create(list=l,name=n)[0]
	hb.sdate=d;hb.save()
	for o in oc:
		Occurence.objects.get_or_create(habit=hb,date=adj[l.freq](o))[0].save()
	return hb

def populate():
	users=[
		{'d':('aapple','applesforever:)','Adam Apples'),'l':(
			{'d':('Rec & Rest','weekly'),'h':(
				('Guitar Practice',dateback(5*7),[dateback(i*7)for i in[1,2,4]]),
				('Meet Friends',dateback(16*7),[dateback(i*7)for i in[2,3,4,6,7,8,10,11,14,15]]),
				('Water Flowers',dateback(2*7),[dateback(i*7)for i in[1,2]])
				)},
			{'d':('Professional Maintenance','monthly'),'h':(
				('Call Coworkers',dateback(31*4),[dateback(i*31)for i in[2,3]]),
				('Tidy Flat',dateback(365),[dateback(i)for i in[364,124,23]])
				)},
			{'d':('Dailies','daily'),'h':(
				('Walk Pony and Blondie',dateback(28),[dateback(i)for i in[1,2,3,5,6,8,9,12,13,14,16,17,19,21,22,25,26,27]]),
				('English Practice',dateback(30),[dateback(i)for i in[3,6,7,9,12,15,16,17,19,24,27,28,30]]),
				('Meditate',dateback(5),[dateback(i)for i in[1,3,4,5]]),
				('Go to Bed Early',dateback(8),[dateback(i)for i in[2,7]])
				)}
			)},
		{'d':('kyle321','1234','Kyle Chambers 😉'),'l':(
			{'d':('Social <:o)','weekly'),'h':(
				('Sports Wednesday',dateback(6*7),[dateback(i*7)for i in[1,3,4,5,6]]),
				('Date w/ Mandie <3',dateback(2*7),[dateback(i*7)for i in[1,2]])
			)},
			{'d':('Self‐care','weekly'),'h':(
				('Early bed',dateback(5*7),[dateback(3*7)]),
				('No fast food',dateback(9*7),[dateback(i*7)for i in[5,6,8,9]])
			)}
		)}
		]
	for u in users:
		usr=addusr(*(u['d']))
		for l in u['l']:
			ls=addls(usr,*(l['d']))
			for h in l['h']:
				addhb(ls,*h)

if __name__=='__main__':
	print('Starting LifeTrack population script…')
	populate()

