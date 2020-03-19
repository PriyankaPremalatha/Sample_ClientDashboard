from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,authenticate
from django.contrib.auth.models import User
# from register.models import UserRegister
from django.core.validators import	validate_email
from supportteamapp.models import OnsiteModel



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

class OnsiteForm(forms.ModelForm):
	organization=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
	sname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
	cperson=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
	purpose=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),required=True,max_length=250)
	appby=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=True)
	workdate=forms.DateField(widget=forms.DateInput(attrs={'class':'form-control','type':'date'}),required=True)
	worktimein=forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control'}),required=True)
	worktimeout=forms.TimeField(input_formats=['%I:%M %p'],widget=forms.TimeInput(attrs={'class':'form-control'}),required=True)
	workdone=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=250)
	description=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),max_length=250)
	proname=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Optional',required=False)
	serialno=forms.IntegerField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Optional',required=False)
	proappby=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),help_text='Optional',required=False)
		


	class Meta:
		model=OnsiteModel
		fields=["organization","sname","cperson","purpose","appby","workdate","worktimein","worktimeout","workdone","description","proname","serialno","proappby"]



	def clean_purpose(self):
		pur=self.cleaned_data("purpose")	
		
		MAX_LENGTH=250
		if len(pur)>MAX_LENGTH:
			raise forms.ValidationError("Maximum %d characters"%MAX_LENGTH)		
		
	def clean_description(self):
		des=self.cleaned_data("description")	
		
		MAX_LENGTH=250
		if len(des)>MAX_LENGTH:
			raise forms.ValidationError("Maximum %d characters"%MAX_LENGTH)		
		
				
			
				
