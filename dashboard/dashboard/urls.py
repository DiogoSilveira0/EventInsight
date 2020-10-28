"""dashboard URL Configuration

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
from django.urls import path
from app import views
from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('home', views.home, name='home'),
    path('people',views.people, name='people'),
    path('parking', views.parking, name='parking'),
    path('sales', views.sales,name='sales'),
    path('wcs',views.wcs,name='wcs'),
    path('activities', views.activities, name='activities'),
    path('meteorology', views.meteorology, name='meteorology'),
    path('gps',views.gps,name='gps'),
    path('queue',views.queue,name='queue')
]
