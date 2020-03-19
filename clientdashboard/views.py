from django.shortcuts import render,redirect
from .forms import RegisterForm,SystemInfoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import SystemInfo
from django.views.generic import ListView
from supportteamapp.models import SystemUpdateInfo
from django.http import JsonResponse
from django.views.generic import View
from django.contrib.auth.decorators import login_required


# Create your views here.
def registerform(request):
	if request.method=="POST":
		form=RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			# messages.success(request,'Registered Successfully')
			return redirect("loginform")	
	else:
		form=RegisterForm()
		
			
	

	return render(request,"registerlogin/registerform.html",{"form":form})
	

def loginform(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect("systemhealth")
		else:
			messages.info(request,"Invalid Username and Password")
			return redirect("loginform")
	else:
		return render(request,"registerlogin/loginform.html")

	


def index(request):
	return render(request,'index.html')	


@login_required(login_url='loginform')
def systemhealth(request):
	total=SystemInfo.objects.count()
	users=SystemInfo.objects.count()
	winupdate=SystemInfo.objects.filter(windowsuptodate='updated').count()
	swupdate=SystemInfo.objects.filter(	softwareupdatetodate='up to date').count()
	hdd=SystemInfo.objects.filter(hardisk='normal').count()
	jabra=SystemInfo.objects.filter(jabradirect='up to date').count()
	winactive=SystemInfo.objects.filter(windowsactivation='activated').count()
	

	evnoerror=SystemInfo.objects.filter(eventviewer='no error').count()
	evtot=SystemInfo.objects.count()
	evres=evtot-evnoerror

	outlook=SystemInfo.objects.count()	
	context={'users':users,'winupdate':winupdate,'total':total,'swupdate':swupdate,'hdd':hdd,'jabra':jabra,'winactive':winactive,'evres':evres,'outlook':outlook}
	return render(request,'dashboard/systemhealth.html',context)	
	
		

@login_required(login_url='loginform')
def systeminfo(request):
	if request.method=="POST":
		form=SystemInfoForm(request.POST)
		if form.is_valid():
			form.save()
			# messages.success(request,'Registered Successfully')
			return redirect("systemhealth")	
	else:
		form=SystemInfoForm()
		
			
	

	return render(request,"dashboard/systeminfo.html",{"form":form})


def index1(request):
	return render(request,'dashboard/index.html')