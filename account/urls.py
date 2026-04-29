from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('log_in/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='logout'),
    path('password_change/',views.change_password,name='pchange'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',html_email_template_name='auth/p_reset_mail.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='auth/p_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='auth/p_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='auth/p_reset_complete.html'), name='password_reset_complete'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('profile/',views.profile,name='profile'),
    path('listing/',views.listing,name='listing'),
    path('mylisting/',views.mylisting,name='mylisting'),
    path('myearning/',views.myearning,name='myearning'),
    path('history/',views.history,name='history'),
    path('notification/',views.notification,name='notification'),
    path('statistics/',views.stats,name='stats'),
    
]
