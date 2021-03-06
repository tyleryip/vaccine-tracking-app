from django.urls import path

from . import views

app_name = 'tracker' # Set the namespace for this app

urlpatterns = [
    # The index view, landing page for the normal user.
    path('', views.index_view, name='index_view'),

    # Login pages for nurse and civilian.
    path('nurse/', views.nurse_login, name='nurse_login'),
    path('civilian/', views.civilian_login, name='civilian_login'),
 
    # Registration pages for new users
    path('civilian/add/', views.new_civilian, name='new_civilian'),
    path('nurse/add/', views.new_nurse, name='new_nurse'),

    # Homepage for civilian user, followed by all additional functionalities.
    path('civilian/<int:hcc_no>/', views.civilian_homepage, name='civilian_homepage'),
    path('civilian/<int:hcc_no>/edit/', views.edit_civilian, name='edit_civilian'),
    path('civilian/<int:hcc_no>/riskfactor/', views.civilian_riskfactor, name='civilian_riskfactor'),
    path('civilian/<int:hcc_no>/appointments/', views.civilian_appointments, name='civilian_appointments'),
    path('civilian/<int:hcc_no>/add_appointment/', views.add_appointment, name='add_appointment'),
    path('civilian/<int:hcc_no>/doctor/', views.civilian_doctor, name='civilian_doctor'),


    # Homepage for nurse user, followed by all additional functionalities.
    path('nurse/<int:hcc_no>/', views.nurse_homepage, name='nurse_homepage'),
    path('nurse/<int:hcc_no>/appointments/', views.nurse_appointments, name='nurse_appointments'),
    path('nurse/vaccines/', views.nurse_vaccines, name='nurse_vaccines'),
    path('nurse/vaccines/<int:DIN_no>/', views.nurse_vaccine_details, name='nurse_vaccine_details'),
    path('nurse/disposal_sites/', views.nurse_disposal_sites, name='nurse_disposal_sites'),
    path('nurse/vaccination_sites/', views.nurse_vaccination_sites, name='nurse_vaccination_sites'),
    path('nurse/<int:hcc_no>/ppe/', views.nurse_ppe, name='nurse_ppe'),
    path('nurse/<int:hcc_no>/edit/', views.edit_nurse, name='edit_nurse'),
]