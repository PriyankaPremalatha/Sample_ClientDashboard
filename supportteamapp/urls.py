from django.urls import path
from supportteamapp import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

urlpatterns=[

	path("sregister/",views.sregister,name="sregister"),
	path("slogin/",views.slogin,name="slogin"),
	path("sinde/",views.sindex,name="sindex"),
	path("onsite/",views.onsite,name="onsites"),
	path("supportindex/systemfile_upload/",views.systemfile_upload,name="systemfile_upload"),
	path("supportindex/onsitefile_upload/",views.onsitefile_upload,name="onsitefile_upload"),
	path("",views.supportindex,name="supportindex"),
	path("orgnameinsertion/",views.OrgnameInsertion.as_view(),name="orgnameinsertion"),
	path("systeminfoinsert/",views.SystemInfoInsert.as_view(),name="systeminfoinsert"),
	path("orgtableview/",views.OrgView.as_view(),name="tableview"),
	path("systemupdate/",views.UpdateSystem.as_view(),name="systemupdates"),
]