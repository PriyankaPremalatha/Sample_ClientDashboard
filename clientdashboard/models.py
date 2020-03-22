from django.db import models
from django.contrib.auth.models import User
from supportteamapp.models import OrgInsertion
# Create your models here.

class SystemInfo(models.Model):

	outlook_choices=(
		('working','Working'),
		('notworking','Not Working'),

		)

	winactivate_choices=(
		('activated','Activated'),
		('notactivated','Not Activated'),

		)

	pdrive_choices=(
		('accessible','Accessible'),
		('notaccessible','Not Accessible'),

		)
	winuptodate_choices=(
		('updated','Updated'),
		('not updated','Not Updated'),

		)

	hdisk_choices=(
		('normal','Normal'),
		('critical','Critical'),

		)
	eviewer_choices=(
		('error','Error'),
		('no error','No Error'),
		('password reqired','Password Required'),
		('power off','Power Off'),
		('office 2016 licensing','office 2016 licensing'),

		)
	jabra_choices=(
		('up to date','Up to date'),
		('not updated','Not Updated'),

		)
	software_choices=(
		('up to date','Up to date'),
		('not updated','Not Updated'),

		)

	sys_user=models.CharField(max_length=100)
	windowsuptodate=models.CharField(max_length=100,choices=winuptodate_choices)
	hardisk=models.CharField(max_length=100,choices=hdisk_choices)
	outlook=models.CharField(max_length=100,choices=outlook_choices)
	eventviewer=models.CharField(max_length=100,choices=eviewer_choices)
	jabradirect=models.CharField(max_length=100,choices=jabra_choices)
	softwareupdatetodate=models.CharField(max_length=100,choices=software_choices)
	pdriveaccess=models.CharField(max_length=100,choices=pdrive_choices)
	windowsactivation=models.CharField(max_length=100,choices=winactivate_choices)
	updated=models.DateField(auto_now=True)
	time=models.TimeField(auto_now=True)


class SystemRequirementModel(models.Model):
	reqpname=models.ForeignKey(OrgInsertion, on_delete=models.CASCADE)
	pname=models.CharField(max_length=100)
	hddtype=models.CharField(max_length=100)
	disksize=models.CharField(max_length=100)
	ndisk=models.CharField(max_length=150)
	cpucore=models.CharField(max_length=100)
	ramsize=models.CharField(max_length=100)
	nmonitors=models.CharField(max_length=100)
	timestamp=models.DateTimeField(auto_now=True)
	