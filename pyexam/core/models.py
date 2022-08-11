from django.db import models
import datetime


# model to store employee's records
class Employee(models.Model):
    STATUS = (
        ('Regular', 'Regular'),
        ('Contractor', 'Contractor'),
    )
    COUNTRY = (
        ('Denmark', 'Denmark'),
        ('Malaysia', 'Malaysia'),
        ('Taiwan', 'Taiwan'),
    )
    emp_id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    emp_status = models.CharField(max_length=255, choices=STATUS)
    country = models.CharField(max_length=255, choices=COUNTRY)
    dob = models.DateTimeField()
