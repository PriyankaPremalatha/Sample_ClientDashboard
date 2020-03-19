from django.shortcuts import render,redirect
from .forms import RegisterForm,OnsiteForm
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView
from django.http import JsonResponse
from django.views.generic import View
from supportteamapp.models import OnsiteModel,OrgInsertion,SystemUpdateModel
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
# Create your views here.
def sregister(request):
	if request.method=="POST":
		form=RegisterForm(request.POST)
		if form.is_valid():
			form.save()
			
			return redirect("slogin")	
	else:
		form=RegisterForm()
	return render(request,"sregisterlogin/supportregister.html",{"form":form})
		

def slogin(request):
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=auth.authenticate(username=username,password=password)
		if user is not None:
			auth.login(request, user)
			return redirect("supportindex")
		else:
			messages.info(request,"Invalid Username and Password")
			return redirect("slogin")
	else:
		return render(request,"sregisterlogin/slogin.html")


# @login_required(login_url='slogin')
	# @staff_member_required(login_url='slogin')
def sindex(request):
	return render(request,"sregisterlogin/sindex.html")

def onsite(request):
	if request.method=="POST":
		form=OnsiteForm(request.POST)
		receiver='priyankapriya3007@gmail.com'
		if form.is_valid():
			name=form.cleaned_data['sname']
			cperson=form.cleaned_data['cperson']
			purpose=form.cleaned_data['purpose']
			workdate=form.cleaned_data['workdate']
			
			form.save()
			send_mail(
				'Subject- On site Info',
				'Name:'+ name + ',\n''Contacted Person:'+ cperson + ',\n''Purpose:'+ purpose + ',\n''Date:'+ str(workdate) + ',\n',
				'dhanalakshmipriyanka3097@gmail.com',
				[

					receiver,
				]


				)
			messages.success(request,'email sent Successfully')
			return redirect("sindex")	
	else:
		form=OnsiteForm()
	return render(request,"dashboard/onsite.html",{"form":form})


@login_required(login_url='slogin')		
def supportindex(request):
	
	organizationobj=OrgInsertion.objects.all()
	context={'organizationobj':organizationobj}
	return render(request,'dashboard/supportindex.html',context=context)



class OrgnameInsertion(View):
	def get(self,request):

			
		organizationname1=request.GET.get('organizationname',None)
		organizationmail1=request.GET.get('organizationmail',None)
		organizationaddr1=request.GET.get('organizationaddr',None)
		organizationphone1=request.GET.get('organizationphone',None)
		print(organizationname1)
		obj=OrgInsertion.objects.create(

			
			organizationname=organizationname1,
			organizationmail=organizationmail1,
			organizationaddr=organizationaddr1,
			organizationphone=organizationphone1,

			)
		print(obj)
		userss={'id':obj.id,
					
					'organizationname':organizationname,
					'organizationmail':organizationmail,
					'organizationaddr':organizationaddr,
					'organizationphone':organizationphone,
					
				}

		data={'userss':userss}

		return JsonResponse(data)


class SystemInfoInsert(View):
	def get(self,request):

		orgname1=request.GET.get('orgname',None)
		sysname1=request.GET.get('sysname',None)
		hddspace1=request.GET.get('hddspace',None)
		ramsize1=request.GET.get('ramsize',None)
		winstatus1=request.GET.get('winstatus',None)
		softwares1=request.GET.get('softwares',None)
		healthstatus1=request.GET.get('healthstatus',None)
		powerstatus1=request.GET.get('powerstatus',None)
		issues1=request.GET.get('issues',None)
		ongoingissues1=request.GET.get('ongoingissues',None)

		
		obj=SystemUpdateModel.objects.create(

			
			orgname=orgname1,
			sysname=sysname1,
			hddspace=hddspace1,
			ramsize=ramsize1,
			winstatus=winstatus1,
			softwares=softwares1,
			healthstatus=healthstatus1,
			powerstatus=powerstatus1,
			issues=issues1,
			ongoingissues=ongoingissues1,

			)
		print(obj)
		userss={'id':obj.id,
					
					'orgname':orgname,
					'sysname':sysname,
					'hddspace':hddspace,
					'ramsize':ramsize,
					'winstatus':winstatus,
					'softwares':softwares,
					'healthstatus':healthstatus,
					'powerstatus':powerstatus,
					'issues':issues,
					'ongoingissues':ongoingissues,
					
				}

		data={'userss':userss}

		return JsonResponse(data)

