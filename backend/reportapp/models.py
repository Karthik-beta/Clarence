from django.db import models


class Gislogs(models.Model):
    id = models.AutoField(primary_key=True)
    idno = models.IntegerField(blank=True, null=True)
    employeeid = models.IntegerField(blank=True, null=True)
    logdate = models.DateField(blank=True, null=True)
    logtime = models.TimeField(blank=True, null=True)
    direction = models.CharField(max_length=50, blank=True, null=True)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    serialno = models.CharField(max_length=50, blank=True, null=True)


class detailsOfEmployees(models.Model):
    employee_id = models.IntegerField()
    device_enroll_id = models.CharField(max_length=100)
    employee_name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=100) #change temperoary to Trainee, Permanent to Confirmed, professionary
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    category = models.CharField(max_length=100)  #Employee type
    status = models.CharField(max_length=100)
    date_of_joining = models.DateField() 

    
# class employeeLogs(models.Model):
#     EMPLOYEE_ID = models.IntegerField(primary_key=True)
#     DIRECTION = models.CharField(max_length=100, blank=True, null=True)
#     SHORTNAME = models.CharField(max_length=100)
#     SERIALNO = models.CharField(max_length=100)
#     LOGDATE = models.DateField(blank=True, null=True)
#     FIRST_LOGTIME = models.DateTimeField(blank=True, null=True)
#     LAST_LOGTIME = models.DateTimeField(blank=True, null=True)
#     TOTAL_LOGTIME = models.DurationField(null=True)

class ProcessedGislogs(models.Model):
    id = models.AutoField(primary_key=True)
    employeeid = models.IntegerField(blank=True, null=True)
    direction = models.CharField(max_length=50, blank=True, null=True)
    shortname = models.CharField(max_length=50, blank=True, null=True)
    serialno = models.CharField(max_length=50, blank=True, null=True)
    logdate = models.DateField(blank=True, null=True)
    first_logtime = models.TimeField(blank=True, null=True)
    last_logtime = models.TimeField(blank=True, null=True)
    total_time = models.DurationField(null=True)
    status = models.CharField(max_length=50, blank=True, null=True)


class employeeDetails(models.Model):
    EMPLOYEE_ID = models.IntegerField(primary_key=True)
    DEVICE_ENROLL_ID = models.CharField(max_length=100)
    EMPLOYEE_NAME = models.CharField(max_length=100)
    COMPANY = models.CharField(max_length=100)
    LOCATION = models.CharField(max_length=100)
    JOB_TYPE = models.CharField(max_length=100)
    DEPARTMENT = models.CharField(max_length=100)
    DESIGNATION = models.CharField(max_length=100)
    CATEGORY = models.CharField(max_length=100)
    STATUS = models.CharField(max_length=100)
    DATE_OF_JOINING = models.DateField()
