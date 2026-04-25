from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('log_in/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='logout'),
    path('password_change/',views.change_password,name='pchange'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('profile/',views.profile,name='profile'),
    path('listing/',views.listing,name='listing'),
    path('mylisting/',views.mylisting,name='mylisting'),
    path('myearning/',views.myearning,name='myearning'),
    path('history/',views.history,name='history'),
    path('notification/',views.notification,name='notification'),
    
]
