from django.urls import path
from clientdashboard import views
from django.conf import settings 
from django.conf.urls.static import static 	
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns=[

	path("registerform",views.registerform,name="registerform"),
	path("",views.loginform,name="loginform"),
	path("index",views.index,name="index"),
	path("index1/",views.index1,name="index1"),
	path("systemrequirement/",views.systemrequirement,name="systemrequirement"),
	path("systemhealth/",views.systemhealth,name="systemhealth"),
	path("systeminfo/",views.systeminfo,name="systeminfo"),
	
	path("systemhealth/requirementfile_upload/",views.requirementfile_upload,name="requirementfile_upload"),
	path('systemreqinsert/',views.SystemRequirementInsert.as_view(), name='systemreqinsert'),
	path('reset-password', PasswordResetView.as_view(), name='password_reset'),
	path('reset-password/done', PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('reset-password/confirm/<uidb64>[0-9A-Za-z]+)-<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('reset-password/complete/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),

	# path('home_view/',views.HomeView.as_view(),name='home_view'),
	path('api/chart/data/',views.ChartData.as_view(),name='chart-data'),
	path('status/',views.status,name='status'),
	path('api/chart/data/department/',views.ChartDataDepartment.as_view(),name='chart-data-department'),
	path('api/chart/data/issue/',views.ChartDataIssues.as_view(),name='chart-data-issue'),
	path('healthysys/',views.healthysys,name='healthysys'),
	path('api/chart/data/sample/',views.ChartDataSample.as_view(),name='chart-data-sample'),
	path('api/chart/data/hddspace/',views.ChartDataHddspace.as_view(),name='chart-data-hddspace'),
	
	path("profile/",views.profile,name="profile"),
	path('api/monthyear/data/',views.MonthYearData.as_view(),name='chart-monthyear-data'),
	# path("profileupload/",views.profileupload,name="profileupload"),
	path('render/pdf/',views.Pdf.as_view()),


]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)