import csv,io
from django.shortcuts import render,redirect
from .forms import RegisterForm,SystemInfoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from clientdashboard.models import SystemInfo,SystemRequirementModel
from django.views.generic import ListView

from django.http import JsonResponse
from supportteamapp.models import OrgInsertion,SystemUpdateModel
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response


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
	organizationobj=OrgInsertion.objects.all()

	sysorgname=request.user.username
	org=OrgInsertion.objects.get(organizationname=sysorgname)
	orgid=org.id
	systotal=SystemUpdateModel.objects.filter(orgname=orgid).count()
	syshealth=SystemUpdateModel.objects.filter(orgname=orgid,healthstatus="Healthy").count()
	
	systemmodel=SystemUpdateModel.objects.filter(orgname=orgid).count()

	sysdata=SystemUpdateModel.objects.filter(orgname=orgid).all()



	context={'organizationobj':organizationobj,'systemmodel':systemmodel,'sysdata':sysdata,'syshealth':syshealth,'systotal':systotal}
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


def systemrequirement(request):
	return render(request,'dashboard/systemrequirement.html')

class SystemRequirementInsert(View):
	def get(self,request):

		name=request.GET.get('reqpname',None)
		reqpname1=OrgInsertion.objects.get(organizationname=name)
		pname1=request.GET.get('pname',None)
		hddtype1=request.GET.get('hddtype',None)
		disksize1=request.GET.get('disksize',None)
		ndisk1=request.GET.get('ndisk',None)
		cpucore1=request.GET.get('cpucore',None)
		ramsize1=request.GET.get('ramsize',None)
		nmonitors1=request.GET.get('nmonitors',None)
		
		

		
		obj=SystemRequirementModel.objects.create(

			
			reqpname=reqpname1,
			pname=pname1,
			hddtype=hddtype1,
			disksize=disksize1,
			ndisk=ndisk1,
			cpucore=cpucore1,
			ramsize=ramsize1,
			nmonitors=nmonitors1,
			

			)
		print(obj)
		userss={'id':obj.id,
					
					'reqpname':reqpname,
					'pname':pname,
					'hddtype':hddtype,
					'disksize':disksize,
					'ndisk':ndisk,
					'cpucore':cpucore,
					'ramsize':ramsize,
					'nmonitors':nmonitors,
					
					
				}

		data={'userss':userss}

		return JsonResponse(data)




def requirementfile_upload(request):
	template="dashboard/systemhealth.html"
	order='order of csv should be Required Person Name'
	context={'order':order}

		
	if request.method=="GET":
		return render(request,template,context)

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
		_, created=SystemRequirementModel.objects.update_or_create(
					reqpname=systemorg,
					pname=column[1],
					hddtype=column[2],
					disksize=column[3],
					ndisk=column[4],
					cpucore=column[5],
					ramsize=column[6],
					nmonitors=column[7],
					
				)
			

	context={}
	return render(request,template,context)


        

        

class ChartData(APIView):
   
    
    def get(self, request, format=None):
    	
    	sysorgname=request.user.username
    	org1=OrgInsertion.objects.get(organizationname=sysorgname)
    	orgid1=org1.id
    	print("******************************************************")
    	print(sysorgname)
    	print(orgid1)
    	syshealth1=SystemUpdateModel.objects.filter(orgname=orgid1,healthstatus="Healthy").count()
    	syshealth2=SystemUpdateModel.objects.filter(orgname=orgid1,healthstatus="Need Attention").count()
    	syshealth3=SystemUpdateModel.objects.filter(orgname=orgid1,healthstatus="Urgent Need Attention").count()
    	syshealth4=SystemUpdateModel.objects.filter(orgname=orgid1,healthstatus="No Maintenance").count()
	    	
    	labels=['Healthy','Need Attention','Urgent Need Attention','No Maintenance']
    	default_items=[syshealth1,syshealth2,syshealth3,syshealth4]
    	data={"labels":labels, "default":default_items}
    	return Response(data)
        


def status(request):
	
	return render(request,'dashboard/status.html')


class ChartDataDepartment(APIView):
   
    
    def get(self, request, format=None):
    	
    	sysorgname=request.user.username
    	org1=OrgInsertion.objects.get(organizationname=sysorgname)
    	orgid1=org1.id
    	

    	sysdepartment=request.GET.get('department',None)
    	syshealth1=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,healthstatus="Healthy").count()
    	syshealth2=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,healthstatus="Need Attention").count()
    	syshealth3=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,healthstatus="Urgent Need Attention").count()
    	syshealth4=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,healthstatus="No Maintenance").count()
	    	
    	labels=['Healthy','Need Attention','Urgent Need Attention','No Maintenance']
    	default_items=[syshealth1,syshealth2,syshealth3,syshealth4]
    	data={"labels":labels, "default":default_items}
    	print(sysdepartment)
    	print(syshealth1,syshealth2,syshealth3,syshealth4)
    	print(default_items)
    	return Response(data)
