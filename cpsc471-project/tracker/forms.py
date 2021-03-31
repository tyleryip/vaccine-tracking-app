#This file will hold the templates for all the forms that pages will have

from django import forms


class hcc_form(forms.Form):
    hcc_no = forms.NumberInput()

