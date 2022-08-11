from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework.views import APIView
from .models import *
from .forms import *
from django.db.models import Count, Q
import pandas as pd

from .serializers import *
from rest_framework.response import Response

# used for accessing database for migrating data
from sqlalchemy import create_engine 

# adding data from excel file to database
def home(request):
    df = pd.read_excel('Employee.xlsx', index_col=0)
    df.index.rename('emp_id', inplace=True)
    df.rename(columns = {
        'First Name':'first_name',
        'Last Name':'last_name',
        'Emp. Status':'emp_status',
        'Country':'country',
        'DOB':'dob',
    }, inplace=True)

    print(df)

    # connect database
    engine = create_engine('sqlite:///db.sqlite3')
    df.to_sql(Employee._meta.db_table, if_exists='replace', con=engine) # using 'replace' to avoid duplicate data
    print('\nDone...\n')

    # passing filter forms to index.html
    forms = FilterForm()
    context = {'forms':forms}

    return render(request, 'index.html', context)

    # However, this will run everytime the page is reload

# GET all employee records
class EmployeeRecords(APIView):
    
    def __init__(self):
        self.employee = Employee.objects.all()

    def get(self, request):
        serializer = EmployeeSerializer(self.employee, many=True) #serialize using DRF

        return Response(serializer.data)

# GET regular employee records   
class RegularEmployee(EmployeeRecords):
    def get(self, request):
        reg_emp = self.employee.filter(emp_status='Regular').values()
        serializer = EmployeeSerializer(reg_emp, many=True)

        return Response(serializer.data)

# GET number of employee different country in descending
class CountryEmployeeCount(EmployeeRecords):
    def get(self, request):
        country_count = self.employee.values('country').annotate(count=Count('country')).order_by('count')[::-1]
        serializer = CountryCountSerializer(country_count, many=True)

        return Response(serializer.data)

# Get employee records based on dynamic filter
class DynamicEmployeeFilter(EmployeeRecords):
    # def get(self, request):
    #     forms = FilterForm()
    #     return HttpResponse(forms)

    def post(self, request):
        forms = FilterForm(data=self.request.POST)

        if forms.is_valid():
            # {'emp_status': 'Regular', 'country': 'Denmark', 'emp_id': None, 'name': '', 'dob_min': datetime.date(1999, 7, 25), 'dob_max': datetime.date(2020, 10, 18)}
            
            filter_emp = self.employee

            # filter status
            if forms.cleaned_data['emp_status'] != '':
                filter_emp = self.employee.filter(emp_status=forms.cleaned_data['emp_status'])
            
            # filter country
            if forms.cleaned_data['country'] != '':
                filter_emp = filter_emp.filter(country=forms.cleaned_data['country'])
            
            # filter employee ID
            if forms.cleaned_data['emp_id'] != None:
                filter_emp = filter_emp.filter(emp_id=forms.cleaned_data['emp_id'])
            
            # filter name
            if forms.cleaned_data['name'] != '':
                # when user enter full name
                if " " in forms.cleaned_data['name']:
                    full_name = forms.cleaned_data['name'].split(" ")
                    # will only take the first and last name for filtering e.g 'John King Doe' -> ['John', 'King', Doe]
                    filter_emp = filter_emp.filter(first_name__contains=full_name[0], last_name__contains=full_name[len(full_name)-1])

                # when user enter first/last name
                else:
                    filter_emp = filter_emp.filter(Q(first_name__contains=forms.cleaned_data['name']) | Q(last_name__contains=forms.cleaned_data['name']))

            
            # filter with range of date
            if forms.cleaned_data['dob_min'] == None:
                forms.cleaned_data['dob_min'] = '1900-1-1'
            if forms.cleaned_data['dob_max'] == None:
                now = datetime.date.today()
                forms.cleaned_data['dob_max'] = now.strftime('%Y-%m-%d')


            filter_emp = filter_emp.filter(dob__range=[forms.cleaned_data['dob_min'], forms.cleaned_data['dob_max']])

            serializer = EmployeeSerializer(filter_emp, many=True)
            return Response(serializer.data)

        else:
            print(forms.errors)
            return Response('error')

        


