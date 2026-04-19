from django.urls import path
from . import views

urlpatterns = [
    path('signup/',views.sign_up,name='sign_up'),
    path('log_in/',views.log_in,name='log_in'),
    path('logout/',views.log_out,name='logout'),
    path('profile_update/',views.profile_update,name='profile_update'),
    path('profile/',views.profile,name='profile')
]
