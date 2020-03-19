from django.urls import path
from clientdashboard import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns=[

	path("registerform",views.registerform,name="registerform"),
	path("loginform/",views.loginform,name="loginform"),
	path("",views.index,name="index"),
	path("index1/",views.index1,name="index1"),
	path("systemhealth/",views.systemhealth,name="systemhealth"),
	path("systeminfo/",views.systeminfo,name="systeminfo"),
	path('reset-password', PasswordResetView.as_view(), name='password_reset'),
	path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),

]