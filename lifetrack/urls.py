from django.urls import path
from lifetrack import views

app_name='lifetrack'

urlpatterns=[
	path('',views.index,name='index'),
	path('index/',views.index,name='index'),
	path('login/',views.login,name='login'),
	path('lists/',views.lists,name='lists'),
	path('addlist/',views.addlist,name='addlist'),
	path('editlist/',views.editlist,name='editlist'),
	path('addhabit/',views.addhabit,name='addhabit'),
	path('edithabit/',views.edithabit,name='edithabit'),
]
