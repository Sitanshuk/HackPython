from django.contrib import admin
from django.urls import re_path
from django.contrib.auth.views import PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
# from django.contrib.auth import views as auth_views
from .views import (
	post_announcement,
	post_forgotpassword,
	post_login,
    post_logout,
	post_register,
	dashboard,
	activate,
    eduloans,
    personalloans,
    homeloans,
    savings,
    current,
    deposit,
    chat,
    readmorei,
    readmoref,
    error,
	)



urlpatterns = [
    re_path(r'^home/$', post_announcement, name = 'home'),
    re_path(r'password_reset/$', PasswordResetView.as_view(), name='password_reset'),
    re_path(r'^password_reset/done/$', PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    re_path(r'^reset/done/$', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    re_path(r'login/$',post_login,name='login'),
    re_path(r'logout/$',post_logout,name='logout'),
    re_path(r'register/$',post_register),
    re_path(r'dashboard/$',dashboard, name = 'dashboard'),
    re_path(r'EducationalLoans/$',eduloans, name = 'eduloans'),
    re_path(r'PersonalLoans/$',personalloans, name = 'personalloans'),
    re_path(r'HomeLoans/$',homeloans, name = 'homeloans'),
    re_path(r'Savings/$',savings, name = 'savings'),
    re_path(r'Current/$',current, name = 'current'),
    re_path(r'Deposit/$',deposit, name = 'deposit'),
    re_path(r'chat/$',deposit, name = 'deposit'),    
    re_path(r'readmorei/$',readmorei, name = 'readmorei'),  
    re_path(r'readmoref/$',readmoref, name = 'readmoref'),  
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',activate, name='activate'),
    # re_path(r'$',error,),


]
