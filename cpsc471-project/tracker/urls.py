from django.urls import path

from . import views

urlpatterns = [
    # This page is the root, you will be presented with two buttons to be able to select which user type you will have
    path('', views.index, name='index'),

    # These pages are for the civilian and nurse login, you'll be presented with a textbox to fill in your HCC and then click a button
    # We will also have to implement a new user section
    path('nurse', views.nurse_login, name='nurse_login'),
    path('civilian', views.civilian_login, name='civilian_login'),

    # After logging in, civilians will be able to access their homepage
    # Ex. civilian/1/
    path('civilian/<int:hcc_no>/', views.civilian_homepage, name='civilian_homepage'),

    path('nurse/<int:hcc_no>/', views.nurse_homepage, name='nurse_homepage')
]