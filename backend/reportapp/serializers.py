from rest_framework import serializers
from .models import Gislogs, ProcessedGislogs, detailsOfEmployees
from django.db.models import Min, Max, OuterRef, Subquery
from datetime import datetime, timedelta, time, date
from django.db.models import Q


class GislogsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Gislogs
        fields = '__all__'


class ProcessedGislogsSerializer(serializers.ModelSerializer):
    first_logtime = serializers.TimeField(format='%H:%M:%S', required=False)
    last_logtime = serializers.TimeField(format='%H:%M:%S', required=False)
    
    class Meta:
        model = ProcessedGislogs
        fields = '__all__'


class detailsOfEmployeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = detailsOfEmployees
        fields = '__all__'
        





# class CombinedLogsSerializer(serializers.Serializer):
#     employeeid = serializers.IntegerField(source='employeeid')
#     logdate = serializers.DateField(source='logdate')
#     logtime = serializers.TimeField(source='logtime')
#     direction = serializers.CharField(source='direction')
#     shortname = serializers.CharField(source='shortname')
#     serialno = serializers.CharField(source='serialno')

#     employee_id = serializers.IntegerField(source='employee.employee_id')
#     device_enroll_id = serializers.CharField(source='employee.device_enroll_id')
#     employee_name = serializers.CharField(source='employee.employee_name')
#     company = serializers.CharField(source='employee.company')
#     location = serializers.CharField(source='employee.location')
#     job_type = serializers.CharField(source='employee.job_type')
#     department = serializers.CharField(source='employee.department')
#     designation = serializers.CharField(source='employee.designation')
#     category = serializers.CharField(source='employee.category')
#     status = serializers.CharField(source='employee.status')
#     date_of_joining = serializers.DateField(source='employee.date_of_joining')

#     def to_representation(self, instance):
#         try:
#             employee = detailsOfEmployees.objects.get(employee_id=instance.employeeid)
#         except detailsOfEmployees.DoesNotExist:
#             employee = None

#         return {
#             'employeeid': instance.employeeid,
#             'logdate': instance.logdate,
#             'logtime': instance.logtime,
#             'direction': instance.direction,
#             'shortname': instance.shortname,
#             'serialno': instance.serialno,
#             'employee_id': employee.employee_id if employee else None,
#             'device_enroll_id': employee.device_enroll_id if employee else None,
#             'employee_name': employee.employee_name if employee else None,
#             'company': employee.company if employee else None,
#             'location': employee.location if employee else None,
#             'job_type': employee.job_type if employee else None,
#             'department': employee.department if employee else None,
#             'designation': employee.designation if employee else None,
#             'category': employee.category if employee else None,
#             'status': employee.status if employee else None,
#             'date_of_joining': employee.date_of_joining if employee else None,
#         }





class CombinedLogsSerializer(serializers.Serializer):
    employeeid = serializers.IntegerField(source='employeeid')
    logdate = serializers.DateField(source='logdate')
    logtime = serializers.TimeField(source='logtime')
    direction = serializers.CharField(source='direction')
    shortname = serializers.CharField(source='shortname')
    serialno = serializers.CharField(source='serialno')

    employee_id = serializers.IntegerField(source='employee.employee_id')
    device_enroll_id = serializers.CharField(source='employee.device_enroll_id')
    employee_name = serializers.CharField(source='employee.employee_name')
    company = serializers.CharField(source='employee.company')
    location = serializers.CharField(source='employee.location')
    job_type = serializers.CharField(source='employee.job_type')
    department = serializers.CharField(source='employee.department')
    designation = serializers.CharField(source='employee.designation')
    category = serializers.CharField(source='employee.category')
    status = serializers.CharField(source='employee.status')
    date_of_joining = serializers.DateField(source='employee.date_of_joining')

    def calculate_overtime(self, first_logtime, last_logtime):
        if first_logtime is not None and first_logtime < time(7, 30):
            morning_overtime_cal = datetime.combine(date.min, time(8, 0)) - datetime.combine(date.min, first_logtime)
            morning_overtime_seconds = int(morning_overtime_cal.total_seconds())
            morning_overtime_minutes = morning_overtime_seconds // 60
        else:
            morning_overtime_minutes = 0

        if last_logtime is not None and last_logtime > time(16, 30):
            evening_overtime_cal = datetime.combine(date.min, last_logtime) - datetime.combine(date.min, time(16, 0))
            evening_overtime_seconds = int(evening_overtime_cal.total_seconds())
            evening_overtime_minutes = evening_overtime_seconds // 60
        else:
            evening_overtime_minutes = 0

        total_overtime_minutes = morning_overtime_minutes + evening_overtime_minutes

        if total_overtime_minutes > 0:
            total_hours, total_minutes = divmod(total_overtime_minutes, 60)
            formatted_overtime = f"{total_hours:02d}:{total_minutes:02d}"
        else:
            formatted_overtime = "00:00"

        return formatted_overtime




    def to_representation(self, instance):
        try:
            employee = detailsOfEmployees.objects.get(employee_id=instance.employeeid)
        except detailsOfEmployees.DoesNotExist:
            employee = None

        # Get the first and last log times for the current employeeid and logdate
        first_log = Gislogs.objects.filter(employeeid=instance.employeeid, logdate=instance.logdate).aggregate(first_logtime=Min('logtime'))
        last_log = Gislogs.objects.filter(employeeid=instance.employeeid, logdate=instance.logdate).aggregate(last_logtime=Max('logtime'))

        first_logtime = first_log['first_logtime']
        last_logtime = last_log['last_logtime']

        # first_logtime = first_log['first_logtime']
        # last_logtime = last_log['last_logtime']

        total_time = None
        if first_logtime and last_logtime:
            time_difference = datetime.combine(datetime.min, last_logtime) - datetime.combine(datetime.min, first_logtime)
            total_seconds = time_difference.total_seconds()
            hours = int(total_seconds // 3600)
            minutes = int((total_seconds % 3600) // 60)
            total_time = f"{hours:02d}:{minutes:02d}"

        late_entry = "00:00"
        if first_logtime is not None and first_logtime > time(8, 15):
            late_difference = datetime.combine(date.min, first_logtime) - datetime.combine(date.min, time(8, 0))
            late_seconds = int(late_difference.total_seconds())
            late_hours, late_remainder = divmod(late_seconds, 3600)
            late_minutes, late_seconds = divmod(late_remainder, 60)
            late_entry = f"{late_hours:02d}:{late_minutes:02d}:{late_seconds:02d}"

        early_exit = "00:00"
        if early_exit is not None and last_logtime < time(15, 45) and last_logtime > first_logtime:
            early_difference = datetime.combine(date.min, time(16, 0)) - datetime.combine(date.min, last_logtime)
            early_seconds = int(early_difference.total_seconds())
            early_hours, early_remainder = divmod(early_seconds, 3600)
            early_minutes, early_seconds = divmod(early_remainder, 60)
            early_exit = f"{early_hours:02d}:{early_minutes:02d}:{early_seconds:02d}"

        overtime = "00:00"
        if first_logtime is not None or last_logtime is not None:
            overtime = self.calculate_overtime(first_logtime, last_logtime)


        shift_status = None
        if first_logtime is not None and total_time > "07:30:00":
            shift_status = "P"
        elif "04:00:00" < total_time <= "07:30:00":
            if first_logtime and last_logtime and first_logtime < time(13, 0) and last_logtime < time(13, 0):
                shift_status = "P/A"
            elif first_logtime and last_logtime and first_logtime > time(13, 0) and last_logtime > time(13, 0):
                shift_status = "A/P"

        if first_logtime == last_logtime:
            shift_status = "A"       
        
        
        return {
                'employeeid': instance.employeeid,
                'logdate': instance.logdate,
                'logtime': instance.logtime,
                'direction': instance.direction,
                'shortname': instance.shortname,
                'serialno': instance.serialno,
                'employee_id': employee.employee_id if employee else None,
                'device_enroll_id': employee.device_enroll_id if employee else None,
                'employee_name': employee.employee_name if employee else None,
                'company': employee.company if employee else None,
                'location': employee.location if employee else None,
                'job_type': employee.job_type if employee else None,
                'department': employee.department if employee else None,
                'designation': employee.designation if employee else None,
                'category': employee.category if employee else None,
                'status': employee.status if employee else "RESIGNED",
                'date_of_joining': employee.date_of_joining if employee else None,
                'first_logtime': first_log['first_logtime'] if first_log['first_logtime'] else None,
                'last_logtime': last_log['last_logtime'] if last_log['last_logtime'] else None,
                'total_time': total_time,
                'late_entry': late_entry,
                'early_exit': early_exit,
                'overtime': overtime,
                'shift_status': shift_status,
            }





class CombinedLogs2Serializer(serializers.Serializer):
    employeeid = serializers.IntegerField(source='employee.employeeid')
    logdate = serializers.DateField(source='employee.logdate')
    logtime = serializers.TimeField(source='employee.logtime')
    direction = serializers.CharField(source='employee.direction')
    shortname = serializers.CharField(source='employee.shortname')
    serialno = serializers.CharField(source='employee.serialno')

    employee_id = serializers.IntegerField(source='employee_id')
    device_enroll_id = serializers.CharField(source='device_enroll_id')
    employee_name = serializers.CharField(source='employee_name')
    company = serializers.CharField(source='company')
    location = serializers.CharField(source='location')
    job_type = serializers.CharField(source='job_type')
    department = serializers.CharField(source='department')
    designation = serializers.CharField(source='designation')
    category = serializers.CharField(source='category')
    status = serializers.CharField(source='status')
    date_of_joining = serializers.DateField(source='date_of_joining')



    def to_representation(self, instance):
        try:
            employee = Gislogs.objects.get(employeeid=instance.employee_id)
        except Gislogs.DoesNotExist:
            employee = None






