from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=128)
	def __str__(σ):
		return σ.user.username

class HabitList(models.Model):
	user=models.ForeignKey(User,on_delete=models.CASCADE)
	name=models.CharField(max_length=128)
	freq=models.CharField(max_length=128)	#Using strings as an enum substitute; we only support predefined frequencies
	def __str__(σ):
		return σ.name
