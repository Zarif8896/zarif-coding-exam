from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):
    dob = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = Employee
        fields = ['emp_id', 'first_name', 'last_name', 'emp_status', 'country', 'dob']

class CountryCountSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()

    class Meta:
        model = Employee
        fields = ['country', 'count']