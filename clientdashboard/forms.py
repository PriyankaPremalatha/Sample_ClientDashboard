from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
# from register.models import UserRegister
from django.core.validators import	validate_email
from clientdashboard.models import SystemInfo

class RegisterForm(UserCreationForm):
	username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'User Name'}),required=True, max_length=50)
	email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),required=True, max_length=50)
	first_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),required=False,help_text='Optional', max_length=50)
	last_name=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),required=False,help_text='Optional', max_length=50)
	is_staff=forms.BooleanField(required=False)
	password1=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),required=True, max_length=50)
	password2=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}),required=True, max_length=50)

	class Meta:
		model=User
		fields=["first_name","last_name","username","email","is_staff","password1","password2"]

	def clean_username(self):
		user=self.cleaned_data["username"]
		try:
			match=User.objects.get(username=user)
		except:
			return self.cleaned_data['username']	
		raise forms.ValidationError("User Name already exists")	

	def clean_email(self):
		email=self.cleaned_data["email"]
		try:
			mt=validate_email(email)
		except:
			return forms.ValidationError("Email is not in correct format")	
		return email

	def clean_confirm_password(self):
		pas=self.cleaned_data("password1")	
		cpas=self.cleaned_data("password2")	
		MIN_LENGTH=8
		if pas!=cpas:
			raise forms.ValidationError("Password and Confirm password not matched")
		else:
			if len(pas)<MIN_LENGTH:
				raise forms.ValidationError("Password should have atleast %d characters"%MIN_LENGTH)		
			if pas.isdigit():
				raise forms.ValidationError("Password should not all numeric")




class SystemInfoForm(forms.ModelForm):
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
		('no error','No Error'),
		('error','Error'),
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
	sys_user=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True, max_length=50)
	softwareupdatetodate=forms.CharField(widget=forms.Select(choices=software_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	windowsuptodate=forms.CharField(widget=forms.Select(choices=winuptodate_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	hardisk=forms.CharField(widget=forms.Select(choices=hdisk_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	outlook=forms.CharField(widget=forms.Select(choices=outlook_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	eventviewer=forms.CharField(widget=forms.Select(choices=eviewer_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	jabradirect=forms.CharField(widget=forms.Select(choices=jabra_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	pdriveaccess=forms.CharField(widget=forms.Select(choices=pdrive_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	windowsactivation=forms.CharField(widget=forms.Select(choices=winactivate_choices,attrs={'class':'form-control'}),required=True, max_length=50)
	class Meta:
		model=SystemInfo
		fields='__all__'



	# def __init__(self,*args,**kwargs):
	# 	super().__init__(*args,*kwargs)
	# 	self.fields['windowsuptodate'].queryset=SystemInfo.objects.none()