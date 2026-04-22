from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/',views.category,name='category'),
    path('host_guide/',views.host_guide,name='host_guide'),
    path('vehicle_detail/<int:id>',views.vehicle_detail,name='vehicle_detail'),
]
