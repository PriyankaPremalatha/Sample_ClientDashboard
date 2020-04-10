from django.shortcuts import render,redirect
import csv,io
from django.http import HttpResponse
# Create your views here.

def loginregisterform(request):
	return render(request,'adminregisterlogin/loginregisterform.html')

