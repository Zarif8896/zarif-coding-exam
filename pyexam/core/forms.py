from django import forms
from .models import *

STATUS = (
    ('', ''),
    ('Regular', 'Regular'),
    ('Contractor', 'Contractor'),
)
COUNTRY = (
    ('', ''),
    ('Denmark', 'Denmark'),
    ('Malaysia', 'Malaysia'),
    ('Taiwan', 'Taiwan'),
)

class FilterForm(forms.Form):
    emp_status = forms.ChoiceField(label='Status', choices=STATUS, required=False)
    country = forms.ChoiceField(label='Country', choices=COUNTRY, required=False)
    emp_id = forms.IntegerField(label='Emp#', required=False)
    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(attrs={'placeholder': 'First Name/Last Name'}),
        required=False
    )
    dob_min = forms.DateField(
        label='DOB minimum',
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}, format='%d/%m/%Y'), 
        input_formats=['%d/%m/%Y'],
        required=False
    )
    dob_max = forms.DateField(
        label='DOB maximum',
        widget=forms.DateInput(attrs={'placeholder': 'dd/mm/yyyy'}, format='%d/%m/%Y'), 
        input_formats=['%d/%m/%Y'],
        required=False
    )
