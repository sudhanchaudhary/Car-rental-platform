from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/',views.category,name='category'),
    path('host_guide/',views.host_guide,name='host_guide'),
    path('listing/',views.listing,name='listing'),
]
