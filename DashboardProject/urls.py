"""DashboardProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from clientdashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("clientdashboard/",include("clientdashboard.urls")),
    path("supportteamapp/",include("supportteamapp.urls")),
    path('api/chart/data/',views.ChartData.as_view(),name='chart-data'),
    path('api/chart/data/department/',views.ChartDataDepartment.as_view(),name='chart-data-department'),
    path('api/chart/data/issue/',views.ChartDataIssues.as_view(),name='chart-data-issue'),
    path('api/chart/data/sample/',views.ChartDataSample.as_view(),name='chart-data-sample'),
    path('api/chart/data/hddspace/',views.ChartDataHddspace.as_view(),name='chart-data-hddspace'),
    path("admindashboard/",include("admindashboard.urls")),
    path('api/monthyear/data/',views.MonthYearData.as_view(),name='chart-monthyear-data'),
]
