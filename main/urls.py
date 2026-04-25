from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('category/',views.category,name='category'),
    path('guide/',views.host_guide,name='host_guide'),
    path('review/',views.review,name='review'),
    path('vehicle_detail/<int:id>',views.vehicle_detail,name='vehicle_detail'),
    path('checkout/add/<int:id>/', views.add_to_checkout, name='add_to_checkout'),
    path('checkout/', views.checkout, name='checkout'),
    path("checkout/update-days/", views.update_checkout_days, name="update_checkout_days"),
]
