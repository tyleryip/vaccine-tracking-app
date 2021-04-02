#This file will hold the templates for all the forms that pages will have

from django import forms


class hcc_form(forms.Form):
    hcc_no = forms.NumberInput()


class civilian_registration_form(forms.Form):
    hcc_no = forms.IntegerField(label = 'civ-hcc')
    phone_no = forms.IntegerField(label = 'phone-no')
    sex = forms.CharField('sex')
    address = forms.CharField(label = 'address', max_length=200)
    age = forms.IntegerField(label = 'age')
    first_name =  forms.CharField(label = 'first-name', max_length=200)
    last_name =  forms.CharField(label = 'last-name', max_length=200)
    doctor_hcc = forms.IntegerField(label = 'doctor-hcc')


class nurse_registration_form(forms.Form):
    hcc_no = forms.IntegerField(label = 'civ-hcc')
    phone_no = forms.IntegerField(label = 'phone-no')
    sex = forms.CharField('sex')
    address = forms.CharField(label = 'address', max_length=200)
    age = forms.IntegerField(label = 'age')
    first_name =  forms.CharField(label = 'first-name', max_length=200)
    last_name =  forms.CharField(label = 'last-name', max_length=200)
    site_address = forms.CharField(label = 'site-address', max_length = 200)

