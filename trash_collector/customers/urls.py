from django.urls import path

from . import views

# TODO: Determine what distinct pages are required for the customer user stories, add a path for each in urlpatterns

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('sign_up/', views.sign_up, name="sign_up"),
    path('change/', views.change, name='change'),
    path('one_time_pickup/', views.one_time_pickup, name='one_time_pickup')
]
