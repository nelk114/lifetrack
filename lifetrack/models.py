from django.db import models
from django.contrib.auth.models import User
from datetime import date

class HabitList(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=128)
	freq=models.CharField(max_length=128)	#Using strings as an enum substitute; we only support predefined frequencies
	def __str__(σ):
		return σ.name

class Habit(models.Model):
	list=models.ForeignKey(HabitList,on_delete=models.CASCADE)
	name=models.CharField(max_length=128)
	sdate=models.DateField(default=date.today)
	def __str__(σ):
		return σ.name

class Occurence(models.Model):
	habit=models.ForeignKey(Habit,on_delete=models.CASCADE)
	date=models.DateField(default=date.today)
	def __str__(σ):
		return f'{s.habit} @ {σ.date}'
