import csv,io
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


@staff_member_required(login_url='slogin')
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

		name=request.GET.get('orgname',None)
		orgname1=OrgInsertion.objects.get(organizationname=name)

		sysname1=request.GET.get('sysname',None)
		department1=request.GET.get('department',None)
		hddspace1=request.GET.get('hddspace',None)
		ramsize1=request.GET.get('ramsize',None)
		winstatus1=request.GET.get('winstatus',None)
		softwares1=request.GET.get('softwares',None)
		healthstatus1=request.GET.get('healthstatus',None)
		powerstatus1=request.GET.get('powerstatus',None)
		issues1=request.GET.get('issues',None)
		ongoingissues1=request.GET.get('ongoingissues',None)

		print(department1)
		obj=SystemUpdateModel.objects.create(

			
			orgname=orgname1,
			sysname=sysname1,
			department=department1,
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
					'department':department,
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

def systemfile_upload(request):
	template="dashboard/supportindex.html"
	prompt={

		'order':'order of csv should be first_name,last_name,email,ip_address,message'

	}
	if request.method=="GET":
		return render(request,template,prompt)

	csv_file=request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request,'this is not an CSV file')	

	data_set=csv_file.read().decode('UTF-8')
	io_string=io.StringIO(data_set)
	next(io_string) 
	for column in csv.reader(io_string, delimiter=',', quotechar='|'):
		sysname=column[0]
		systemorg=OrgInsertion.objects.get(organizationname=sysname)
		print(systemorg)
		_, created=SystemUpdateModel.objects.update_or_create(
					orgname=systemorg,
					sysname=column[1],
					department=column[2],
					hddspace=column[3],
					ramsize=column[4],
					winstatus=column[5],
					softwares=column[6],
					healthstatus=column[7],
					powerstatus=column[8],
					issues=column[9],
					ongoingissues=column[10],
				)
			

	context={}
	return render(request,template,context)

		
def onsitefile_upload(request):
	template="dashboard/supportindex.html"
	prompt={

		'order':'order of csv should be first_name,last_name,email,ip_address,message'

	}
	if request.method=="GET":
		return render(request,template,prompt)

	csv_file=request.FILES['file']

	if not csv_file.name.endswith('.csv'):
		messages.error(request,'this is not an CSV file')	

	data_set=csv_file.read().decode('UTF-8')
	io_string=io.StringIO(data_set)
	next(io_string) 
	for column in csv.reader(io_string, delimiter=',', quotechar='|'):
		
		
		_, created=OnsiteModel.objects.update_or_create(
					organization=column[0],
					sname=column[1],
					cperson=column[2],
					purpose=column[3],
					appby=column[4],
					workdate=column[5],
					worktimein=column[6],
					worktimeout=column[7],
					workdone=column[8],
					description=column[9],
					proname=column[10],
					serialno=column[11],
					proappby=column[12],

				)
			

	context={}
	return render(request,template,context)
		
		