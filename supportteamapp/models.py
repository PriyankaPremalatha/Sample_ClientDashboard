from django.db import models


# Create your models here.
class OnsiteModel(models.Model):
	organization=models.CharField(max_length=100)
	sname=models.CharField(max_length=100,null=True)
	cperson=models.CharField(max_length=100,null=True)
	purpose=models.CharField(max_length=500,null=True)
	appby=models.CharField(max_length=100,null=True)
	workdate=models.DateField(null=True)
	worktimein=models.TimeField(null=True)
	worktimeout=models.TimeField(null=True)
	workdone=models.CharField(max_length=500,null=True)
	description=models.CharField(max_length=500,null=True)
	proname=models.CharField(max_length=100,blank=True,null=True)
	serialno=models.IntegerField(blank=True,null=True)
	proappby=models.CharField(max_length=100,blank=True,null=True)
	timestamp=models.DateTimeField(auto_now=True,null=True)




class OrgInsertion(models.Model):
	organizationname=models.CharField(max_length=100)
	organizationmail=models.CharField(max_length=100)
	organizationaddr=models.CharField(max_length=100)
	organizationphone=models.CharField(max_length=100)

	def __str__(self):
		return self.organizationname

class SystemUpdateModel(models.Model):

	orgname=models.ForeignKey(OrgInsertion, on_delete=models.CASCADE)
	sysname=models.CharField(max_length=150)
	department=models.CharField(max_length=150)
	hddspace=models.CharField(max_length=150)
	ramsize=models.CharField(max_length=150)
	winstatus=models.CharField(max_length=150)
	softwares=models.CharField(max_length=1000)
	healthstatus=models.CharField(max_length=150)
	powerstatus=models.CharField(max_length=150)
	issues=models.CharField(max_length=1000,blank=True,null=True)
	ongoingissues=models.CharField(max_length=1000,blank=True,null=True)
	timestamp=models.DateTimeField(auto_now=True)

	

