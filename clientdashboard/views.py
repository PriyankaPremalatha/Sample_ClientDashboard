import csv,io
from django.shortcuts import render,redirect
from .forms import RegisterForm,SystemInfoForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User,auth
from django.contrib import messages
from clientdashboard.models import SystemInfo,SystemRequirementModel
from django.views.generic import ListView
from django.utils import timezone
from django.http import JsonResponse
from supportteamapp.models import OrgInsertion,SystemUpdateModel
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import TruncMonth as Month, TruncYear as Year
from django.http import HttpResponse
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta
import datetime
import calendar
from .render import Render
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

	

@login_required(login_url='loginform')
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


	sysonissues=SystemUpdateModel.objects.filter(Q(ongoingissues='None'),Q(ongoingissues='')).count()

	context={'organizationobj':organizationobj,'systemmodel':systemmodel,'sysdata':sysdata,'syshealth':syshealth,'systotal':systotal,'sysonissues':sysonissues}
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
					
					'reqpname':obj.reqpname,
					'pname':obj.pname,
					'hddtype':obj.hddtype,
					'disksize':obj.disksize,
					'ndisk':obj.ndisk,
					'cpucore':obj.cpucore,
					'ramsize':obj.ramsize,
					'nmonitors':obj.nmonitors,
					
					
				}

		data={'userss':list(userss)}

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
    	
    	fromdate=request.GET.get('fromdate',None)
    	todate=request.GET.get('todate',None)
    
    	# start_date = datetime.date(2020,3,31)
    	# end_date = datetime.date(2020,4,30)
    	sd = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
    	print(sd)
    	
    	print("================================================----------------------------===========================")
    	start_date = datetime.datetime.strptime(fromdate, '%Y-%m-%d')
    	monthname=start_date.strftime("%B")
    	start_date -= datetime.timedelta(days=1)
    	end_date = datetime.datetime.strptime(todate, '%Y-%m-%d')
    	result=end_date-start_date	
    	issue_array1=[]
    	issue_array2=[]
    	issue_array3=[]
    	issue_array4=[]
    	for i in range(result.days):
    		start_date += datetime.timedelta(days=1)
    		issue1=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="None").count()
    		issue2=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="Error").count()
    		issue3=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="Office 2016 licensing").count()
    		issue4=SystemUpdateModel.objects.filter(~Q(issues='None'),~Q(issues='Error'),~Q(issues='Office 2016 licensing'),~Q(issues=''),orgname=orgid1,date=start_date).count()
    		issue_array1.append(issue1)
    		issue_array2.append(issue2)
    		issue_array3.append(issue3)
    		issue_array4.append(issue4)
	    	
    	labels=['No Error','Error','Office 2016 licensing Error','Others']
    	
    	data={'labels':labels,'issue_array1':issue_array1,'issue_array2':issue_array2,'issue_array3':issue_array3,'issue_array4':issue_array4,'m_name':monthname}
    	print(issue_array1)
    
    	return Response(data)    



def status(request):
	organizationobj=OrgInsertion.objects.all()
		
	return render(request,'dashboard/status.html',{"organizationobj":organizationobj})


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

    	issue1=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,issues='None').count()
    	issue2=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,issues="Error").count()
    	issue3=SystemUpdateModel.objects.filter(orgname=orgid1,department=sysdepartment,issues="Office 2016 licensing").count()
    	issue4=SystemUpdateModel.objects.filter(~Q(issues='None'),~Q(issues='Error'),~Q(issues='Office 2016 licensing'),~Q(issues=''),~Q(issues='No Error'),orgname=orgid1).count()
	    

    	labels=['Healthy','Need Attention','Urgent Need Attention','No Maintenance']
    	default_items=[syshealth1,syshealth2,syshealth3,syshealth4]

    	issuelabels=['No Error','Error','Office 2016 licensing Error','Others']
    	depissues=[issue1,issue2,issue3,issue4]
    	
    	data={"labels":labels, "default":default_items,'sysdepartment':sysdepartment,"deplabels":issuelabels,"depissues":depissues}
    	
    	return Response(data)


class ChartDataIssues(APIView):
   
    
    def get(self, request, format=None):
    	
    	sysorgname=request.user.username
    	org1=OrgInsertion.objects.get(organizationname=sysorgname)
    	orgid1=org1.id
    	

    	
    	issue1=SystemUpdateModel.objects.filter(orgname=orgid1,issues='None').count()
    	issue2=SystemUpdateModel.objects.filter(orgname=orgid1,issues="Error").count()
    	issue3=SystemUpdateModel.objects.filter(orgname=orgid1,issues="Office 2016 licensing").count()
    	issue4=SystemUpdateModel.objects.filter(~Q(issues='None'),~Q(issues='Error'),~Q(issues='Office 2016 licensing'),~Q(issues=''),~Q(issues='No Error'),orgname=orgid1).count()
    	
	    	
    	labels=['No Error','Error','Office 2016 licensing Error','Others']
    	default_items=[issue1,issue2,issue3,issue4]
    	
    	

    	data={"labels":labels, "default":default_items}
    	
    	
    	print(default_items)
    	return Response(data)

@login_required(login_url='loginform')
def healthysys(request):

	sysorgname=request.user.username
	org=OrgInsertion.objects.get(organizationname=sysorgname)
	orgid=org.id
	healthysys=SystemUpdateModel.objects.filter(orgname=orgid,healthstatus="Healthy")
	organizationobj=OrgInsertion.objects.all()

	systotal=SystemUpdateModel.objects.filter(orgname=orgid).count()
	syshealth=SystemUpdateModel.objects.filter(orgname=orgid,healthstatus="Healthy").count()
	
	systemmodel=SystemUpdateModel.objects.filter(orgname=orgid).count()

	sysdata=SystemUpdateModel.objects.filter(orgname=orgid).all()

	sysonissues=SystemUpdateModel.objects.filter(Q(ongoingissues='None'),Q(ongoingissues=''),orgname=orgid).count()

	context={'healthysys':healthysys,'organizationobj':organizationobj,'systemmodel':systemmodel,'sysdata':sysdata,'syshealth':syshealth,'systotal':systotal,'sysonissues':sysonissues}
	return render(request,'dashboard/healthysys.html',context)


class ChartDataSample(APIView):
   
    
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
    	data={"labels1":labels, "default1":default_items}
    	return Response(data)

class ChartDataHddspace(APIView):
   
    
    def get(self, request, format=None):
    	
    	sysorgname=request.user.username
    	org1=OrgInsertion.objects.get(organizationname=sysorgname)
    	orgid1=org1.id
    	
    	diskhealth1=SystemUpdateModel.objects.filter(orgname=orgid1,hddspace="Normal").count()
    	diskhealth2=SystemUpdateModel.objects.filter(orgname=orgid1,hddspace="Critical").count()
    		
    	labels=['Normal','Critical']
    	default_items=[diskhealth1,diskhealth2]
    	data={"disklabels":labels, "diskdefault":default_items}
    	return Response(data)



def profile(request):
	return render(request,'dashboard/profile.html')

# def profileupload(request):
# 	if request.method == 'POST':
# 		user_form = UserForm(request.POST, instance=request.user)
# 		profile_form = ProfileForm(request.POST,request.FILES, instance=request.user.profile)
# 		if user_form.is_valid() and profile_form.is_valid():
# 			user_form.save()
# 			profile_form.save()
# 			messages.success(request,'Uploaded Successfully')
# 			return redirect('systemhealth')
# 		else:
# 			messages.error(request, 'systemhealth.html',('Please correct the error below.'))
# 	else:
# 		user_form = UserForm(instance=request.user)
# 		profile_form = ProfileForm(instance=request.user.profile)
# 	return render(request, 'systemhealth.html', {
#         'user_form': user_form,
#         'profile_form': profile_form
#     })


class MonthYearData(APIView):
   
    
    def get(self, request, format=None):
    	
    	sysorgname=request.user.username
    	org1=OrgInsertion.objects.get(organizationname=sysorgname)
    	orgid1=org1.id
    	
    	m1=request.GET.get('monthdate',None)
    	y1=request.GET.get('yeardate',None)

    	_, num_days = calendar.monthrange(int(y1), int(m1))
    	first_day = datetime.date(int(y1), int(m1), 1)
    	last_day = datetime.date(int(y1), int(m1), num_days)

    	fd=first_day.strftime('%Y-%m-%d')
    	ld=last_day.strftime('%Y-%m-%d')
    	
    	
    	print("================================================----------------------------===========================")
    	start_date = datetime.datetime.strptime(fd, '%Y-%m-%d')
    	monthname=start_date.strftime("%B")
    	start_date -= datetime.timedelta(days=1)
    	end_date = datetime.datetime.strptime(ld, '%Y-%m-%d')
    	result=end_date-start_date	
    	issue_array1=[]
    	issue_array2=[]
    	issue_array3=[]
    	issue_array4=[]
    	for i in range(result.days):
    		start_date += datetime.timedelta(days=1)
    		issue1=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="None").count()
    		issue2=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="Error").count()
    		issue3=SystemUpdateModel.objects.filter(date=start_date,orgname=orgid1,issues="Office 2016 licensing").count()
    		issue4=SystemUpdateModel.objects.filter(~Q(issues='None'),~Q(issues='Error'),~Q(issues='Office 2016 licensing'),~Q(issues=''),orgname=orgid1,date=start_date).count()
    		issue_array1.append(issue1)
    		issue_array2.append(issue2)
    		issue_array3.append(issue3)
    		issue_array4.append(issue4)
	    	
    	labels=['No Error','Error','Office 2016 licensing Error','Others']
    	
    	data={'labels':labels,'issue_array1':issue_array1,'issue_array2':issue_array2,'issue_array3':issue_array3,'issue_array4':issue_array4,'m_name':monthname}
    	print(issue_array1)
    
    	return Response(data)    



class Pdf(View):
    def get(self,request):
         sysorgname=request.user.username
         org1=OrgInsertion.objects.get(organizationname=sysorgname)
         orgid1=org1.id
         data1=SystemUpdateModel.objects.filter(orgname=orgid1).all() 
         today = timezone.now()

         params = {
        'data1': data1,
        'today': today,
        'request': request,
         }
         return Render.render('dashboard/pdffile.html', params)
    
        
   
    
     
            
   
    
    

    
   

   