from django.urls import path

from . import views

app_name = 'tracker' # Set the namespace for this app

urlpatterns = [
    # This page is the root, you will be presented with two buttons to be able to select which user type you will have
    path('', views.index_view, name='index_view'),

    # These pages are for the civilian and nurse login, you'll be presented with a textbox to fill in your HCC and then click a button
    # We will also have to implement a new user section
    path('nurse/', views.nurse_login, name='nurse_login'),
    path('civilian/', views.civilian_login, name='civilian_login'),

    # After logging in, civilians will be able to access their homepage
    # Ex. civilian/1/
    path('civilian/<int:hcc_no>/', views.civilian_homepage, name='civilian_homepage'),
    path('civilian/add/', views.new_civilian, name='new_civilian'),
    path('civilian/<int:hcc_no>/edit', views.edit_civilian, name='edit_civilian'),
    path('civilian/<int:hcc_no>/riskfactor', views.civilian_riskfactor, name='civilian_riskfactor'),

    # After logging in, nurse will be able to access their homepage
    # Ex. nurse/1/
    path('nurse/<int:hcc_no>/', views.nurse_homepage, name='nurse_homepage'),
    path('nurse/add/', views.new_nurse, name='new_nurse'),
    path('nurse/<int:hcc_no>/edit', views.edit_nurse, name='edit_nurse'),
]