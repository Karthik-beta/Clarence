from django.shortcuts import render
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from datetime import time, datetime, date, timedelta
from django.db.models import Count, Case, When, Value, CharField, F
from django.utils import timezone
from django.db.models import Q
from django.db.models import Min, Max, Subquery
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from rest_framework.pagination import PageNumberPagination
from rest_framework.pagination import CursorPagination
from rest_framework import filters
from django_filters import rest_framework as filters
from rest_framework import viewsets, generics
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


from .models import ProcessedGislogs, detailsOfEmployees, Gislogs


import reportapp.models as models
import reportapp.serializers as serializers
from reportapp.serializers import ( ProcessedGislogsSerializer, 
                                   detailsOfEmployeesSerializer, 
                                   GislogsSerializer,
                                   CombinedLogsSerializer,
                                #    EmployeeLogSerializer,
                                    CombinedDetailsSerializer,
                                   
                                  )


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def rawDataApi(request, id=0):
    if request.method == 'GET':
        rawData = models.RawData.objects.all()
        rawData_serializer = serializers.RawDataSerializer(rawData, many=True)
        return JsonResponse(rawData_serializer.data, safe=False)
    elif request.method == 'POST':
        rawData_data = JSONParser().parse(request)
        rawData_serializer = serializers.RawDataSerializer(data=rawData_data)
        if rawData_serializer.is_valid():
            rawData_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        rawData_data = JSONParser().parse(request)
        rawData = models.RawData.objects.get(id=rawData_data['id'])
        rawData_serializer = serializers.RawDataSerializer(rawData, data=rawData_data)
        if rawData_serializer.is_valid():
            rawData_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        rawData = models.RawData.objects.get(id=id)
        rawData.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def processedDataApi(request, id=0):
    if request.method == 'GET':
        processedData = models.ProcessedData.objects.all()
        processedData_serializer = serializers.ProcessedDataSerializer(processedData, many=True)
        return JsonResponse(processedData_serializer.data, safe=False)
    elif request.method == 'POST':
        processedData_data = JSONParser().parse(request)
        processedData_serializer = serializers.ProcessedDataSerializer(data=processedData_data)
        if processedData_serializer.is_valid():
            processedData_serializer.save()
            return JsonResponse("Added Successfully", safe=False)
        return JsonResponse("Failed to Add", safe=False)
    elif request.method == 'PUT':
        processedData_data = JSONParser().parse(request)
        processedData = models.ProcessedData.objects.get(id=processedData_data['id'])
        processedData_serializer = serializers.ProcessedDataSerializer(processedData, data=processedData_data)
        if processedData_serializer.is_valid():
            processedData_serializer.save()
            return JsonResponse("Updated Successfully", safe=False)
        return JsonResponse("Failed to Update")
    elif request.method == 'DELETE':
        processedData = models.ProcessedData.objects.get(id=id)
        processedData.delete()
        return JsonResponse("Deleted Successfully", safe=False)
    




from rest_framework.response import Response
from rest_framework import status

class EmployeeDetailView(APIView):
    def get(self, request, employee_id, format=None):
        try:
            # Look up employee details in both tables
            # table1_entries = ProcessedGislogs.objects.filter(employeeid=employee_id)
            # table2_entry = detailsOfEmployees.objects.get(employee_id=employee_id)
            print("Fetching data from table1...")
            table1_entries = ProcessedGislogs.objects.filter(employeeid=employee_id)
            print("Fetching data from table2...")
            table2_entry = detailsOfEmployees.objects.get(employee_id=employee_id)
            
            
            # Construct the response data for table2
            response_data = {
                "employee_id": employee_id,
                "table1_data": [],
                "device_enroll_id": table2_entry.device_enroll_id,
                "employee_name": table2_entry.employee_name,
                "company": table2_entry.company,
                "location": table2_entry.location,
                "job_type": table2_entry.job_type,
                "department": table2_entry.department,
                "designation": table2_entry.designation,
                "category": table2_entry.category,
                "status": table2_entry.status,
                "date_of_joining": table2_entry.date_of_joining,
            }
            
            # Add table1 entries to the response data
            for entry in table1_entries:
                response_data["table1_data"].append({
                    "direction": entry.direction,
                    "shortname": entry.shortname,
                    "serialno": entry.serialno,
                    "logdate": entry.logdate,
                    "first_logtime": entry.first_logtime,
                    "last_logtime": entry.last_logtime,
                })
            
            return Response(response_data, status=status.HTTP_200_OK)
        
        # except (ProcessedGislogs.DoesNotExist, detailsOfEmployees.DoesNotExist):
        #     return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        except ProcessedGislogs.DoesNotExist:
            print("ProcessedGislogs.DoesNotExist")
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except detailsOfEmployees.DoesNotExist:
            print("detailsOfEmployees.DoesNotExist")
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)





# class AllEmployeesView(APIView):
#     def get(self, request, format=None):
#         try:
#             employees = detailsOfEmployees.objects.all()
#             processed_data = ProcessedGislogs.objects.all()

#             employees_serializer = detailsOfEmployeesSerializer(employees, many=True)
#             processed_data_serializer = ProcessedGislogsSerializer(processed_data, many=True)

#             response_data = {
#                 "employees": employees_serializer.data,
#                 "processed_data": processed_data_serializer.data
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except detailsOfEmployees.DoesNotExist or ProcessedGislogs.DoesNotExist:
#             return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)



class AllEmployeesView(APIView):
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, format=None):
        try:
            employees = detailsOfEmployees.objects.all()
            processed_data = ProcessedGislogs.objects.all()

            employees_serializer = detailsOfEmployeesSerializer(employees, many=True)
            processed_data_serializer = ProcessedGislogsSerializer(processed_data, many=True)

            processed_data_with_status = []
            for entry in processed_data_serializer.data:
                first_logtime = entry["first_logtime"]
                last_logtime = entry["last_logtime"]
                total_time = entry["total_time"]

                if first_logtime and last_logtime:
                    if total_time < "04:00:00":
                        entry["attendance"] = "A"    #if first_logtime < "13:00:00" and last_logtime < "13:00:00":                   entry["attendance"] = "P/A"               elif first_logtime >= "13:00:00" and last_logtime >= "13:00:00":                       entry["attendance"] = "A/P"
                    elif total_time >= "04:00:00":
                        entry["attendance"] = "P"
                    else:
                        entry["attendance"] = "P"
                else:
                    entry["attendance"] = "A"
                processed_data_with_status.append(entry)

            response_data = {
                "employees": employees_serializer.data,
                "processed_data": processed_data_with_status
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except (detailsOfEmployees.DoesNotExist, ProcessedGislogs.DoesNotExist):
            return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)
        




# class EmployeePresenceView(APIView):
#     # @method_decorator(cache_page(60 * 5))
#     def get(self, request, format=None):
#         try:
#             # Get the minimum and maximum log dates from the database
#             date_range = ProcessedGislogs.objects.aggregate(min_date=Min('logdate'), max_date=Max('logdate'))

#             # Calculate the date 7 days ago from the maximum log date
#             end_date = date_range['max_date']
#             start_date = end_date - timedelta(days=4)

#             # Query the database to get the presence and absence count for each day
#             presence_data = ProcessedGislogs.objects.filter(logdate__range=(start_date, end_date)) \
#                 .values('logdate') \
#                 .annotate(present_count=Count('id', filter=~Q(first_logtime__isnull=True) & ~Q(last_logtime__isnull=True)),
#                           absent_count=Count('id', filter=Q(first_logtime__isnull=True) | Q(last_logtime__isnull=True)))

#             # Process the data to create a list of dictionaries, each containing "date", "present_count", and "absent_count"
#             presence_count = []
#             for entry in presence_data:
#                 logdate = entry['logdate']
#                 present_count = entry['present_count']
#                 absent_count = entry['absent_count']

#                 presence_count.append({
#                     "date": logdate.strftime('%Y-%m-%d'),
#                     "present_count": present_count,
#                     "absent_count": absent_count
#                 })

#             # Fill in missing dates with zero counts
#             current_date = start_date
#             while current_date <= end_date:
#                 if not any(entry['date'] == current_date.strftime('%Y-%m-%d') for entry in presence_count):
#                     presence_count.append({
#                         "date": current_date.strftime('%Y-%m-%d'),
#                         "present_count": 0,
#                         "absent_count": 0
#                     })
#                 current_date += timedelta(days=1)

#             # Sort the presence_count list by date
#             sorted_presence_count = sorted(presence_count, key=lambda x: x['date'])

#             response_data = {
#                 "presence_count": sorted_presence_count
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         except ProcessedGislogs.DoesNotExist:
#             return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)


class EmployeePresenceView(APIView):
    # @method_decorator(cache_page(60 * 5))
    def get(self, request, format=None):
        try:
            # Get the minimum and maximum log dates from the database
            date_range = ProcessedGislogs.objects.aggregate(min_date=Min('logdate'), max_date=Max('logdate'))

            # Calculate the date 7 days ago from the maximum log date
            end_date = date_range['max_date']
            start_date = end_date - timedelta(days=30)

            # Query the database to get the presence and absence count for each day
            presence_data = ProcessedGislogs.objects.filter(logdate__range=(start_date, end_date)) \
                .values('logdate') \
                .annotate(present_count=Count('id', filter=~Q(first_logtime__isnull=True) & ~Q(last_logtime__isnull=True)),
                          absent_count=Count('id', filter=Q(first_logtime__isnull=True) | Q(last_logtime__isnull=True)),
                          late_entry_count=Count('id', filter=Q(first_logtime__isnull=False) & Q(first_logtime__gt=time(8, 15))),
                          early_exit_count=Count('id', filter=Q(last_logtime__isnull=False) & Q(last_logtime__lt=time(15, 45)) & Q(last_logtime__gt=F('first_logtime'))),
                          overtime_count=Count('id', filter=Q(first_logtime__isnull=False) | Q(last_logtime__isnull=False)))

            # Process the data to create a list of dictionaries, each containing "date" and counts
            presence_count = []
            for entry in presence_data:
                logdate = entry['logdate']
                present_count = entry['present_count']
                absent_count = entry['absent_count']
                late_entry_count = entry['late_entry_count']
                early_exit_count = entry['early_exit_count']
                overtime_count = entry['overtime_count']

                presence_count.append({
                    "date": logdate.strftime('%Y-%m-%d'),
                    "present_count": present_count,
                    "absent_count": absent_count,
                    "late_entry_count": late_entry_count,
                    "early_exit_count": early_exit_count,
                    "overtime_count": overtime_count
                })

            # Fill in missing dates with zero counts
            current_date = start_date
            while current_date <= end_date:
                if not any(entry['date'] == current_date.strftime('%Y-%m-%d') for entry in presence_count):
                    presence_count.append({
                        "date": current_date.strftime('%Y-%m-%d'),
                        "present_count": 0,
                        "absent_count": 0,
                        "late_entry_count": 0,
                        "early_exit_count": 0,
                        "overtime_count": 0
                    })
                current_date += timedelta(days=1)

            # Sort the presence_count list by date
            sorted_presence_count = sorted(presence_count, key=lambda x: x['date'])

            response_data = {
                "presence_count": sorted_presence_count
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ProcessedGislogs.DoesNotExist:
            return Response({"error": "No data found"}, status=status.HTTP_404_NOT_FOUND)


# class AttendanceStatisticsAPIView(APIView):
#     # @method_decorator(cache_page(60 * 5))
#     def get(self, request, *args, **kwargs):
#         # Calculate the latest date in the database
#         latest_date = ProcessedGislogs.objects.latest('logdate').logdate

#         # Define conditions for late entry and early exit
#         late_entry_condition = Q(first_logtime__gt="08:15:00") & Q(first_logtime__lt="13:00:00")
#         early_exit_condition = Q(last_logtime__gt="13:00:00") & Q(last_logtime__lt="15:45:00")

#         # Query to calculate statistics
#         attendance_stats = ProcessedGislogs.objects.filter(logdate=latest_date).annotate(
#             attendance_status=Case(
#                 When(late_entry_condition, then=Value('Late Entry')),
#                 When(early_exit_condition, then=Value('Early Exit')),
#                 When(first_logtime__isnull=True, last_logtime__isnull=True, then=Value('Absent')),
#                 default=Value('Present'),
#                 output_field=CharField()
#             )
#         ).values('attendance_status').annotate(count=Count('id'))

#         # Prepare the response data
#         response_data = { 
#             'latest_date': latest_date,
#             'attendance_stats': list(attendance_stats)
#         }

#         return Response(response_data)
    


class AttendanceStatisticsAPIView(APIView):
    # @method_decorator(cache_page(60 * 5))
    def get(self, request, *args, **kwargs):
        # Calculate the latest date in the database
        latest_date = ProcessedGislogs.objects.latest('logdate').logdate

        # Define conditions for late entry and early exit
        late_entry_condition = Q(first_logtime__gt="08:15:00") & Q(first_logtime__lt="13:00:00")
        early_exit_condition = Q(last_logtime__gt="13:00:00") & Q(last_logtime__lt="15:45:00")

        # Query to calculate statistics
        attendance_stats = ProcessedGislogs.objects.filter(logdate=latest_date).annotate(
            attendance_status=Case(
                When(late_entry_condition, then=Value('Late Entry')),
                When(early_exit_condition, then=Value('Early Exit')),
                When(first_logtime__isnull=True, last_logtime__isnull=True, then=Value('Absent')),
                default=Value('Present'),
                output_field=CharField()
            )
        ).values('attendance_status').annotate(count=Count('id'))

        # Create a dictionary to store attendance status counts
        attendance_counts = {}

        # Populate the dictionary with counts
        for stat in attendance_stats:
            attendance_counts[stat['attendance_status']] = stat['count']

        # Prepare the response data
        response_data = {
            'latest_date': latest_date,
            'attendance_stats': [attendance_counts]
        }

        return Response(response_data)




class AttendanceStatistics2APIView(APIView):
    # @method_decorator(cache_page(60 * 5))
    def get(self, request, *args, **kwargs):
        # Calculate the latest date in the database
        latest_date = ProcessedGislogs.objects.latest('logdate').logdate

        # Define conditions for late entry and early exit
        late_entry_condition = Q(first_logtime__gt="08:00:00") & Q(first_logtime__lt="13:00:00")
        early_exit_condition = Q(last_logtime__gt="13:00:00") & Q(last_logtime__lt="16:00:00")
        live_headcount_condition = Q(first_logtime=F('last_logtime'))

        # Query to calculate statistics
        attendance_stats = ProcessedGislogs.objects.filter(logdate=latest_date).annotate(
            attendance_status=Case(
                When(late_entry_condition, then=Value('Late Entry')),
                When(early_exit_condition, then=Value('Early Exit')),
                When(first_logtime__isnull=True, last_logtime__isnull=True, then=Value('Absent')),
                When(live_headcount_condition, then=Value('Live Headcount')),
                default=Value('Present'),
                output_field=CharField()
            )
        ).values('attendance_status').annotate(count=Count('id'))

        # Prepare the response data
        response_data = { 
            'latest_date': latest_date,
            'attendance_stats': list(attendance_stats)
        }

        return Response(response_data)
    


class FirstLastLogTimeView(APIView):
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, format=None):
        # Get the queryset to calculate the first and last logtimes for each employee on each logdate
        queryset = Gislogs.objects.order_by('-logdate', 'employeeid')

        # Create a dictionary to hold the calculated logtimes for each (employeeid, logdate) pair
        logtimes_dict = {}

        # Loop through the queryset to calculate logtimes
        for entry in queryset:
            employee_id = entry.employeeid
            log_date = entry.logdate

            if (employee_id, log_date) not in logtimes_dict:
                if entry.logtime < time(16, 0):
                    first_logtime = entry.logtime
                else:
                    first_logtime = None

                logtimes_dict[(employee_id, log_date)] = {
                    'first_logtime': first_logtime,
                    'last_logtime': entry.logtime,
                    'logs': [],
                }
            else:
                logtimes_dict[(employee_id, log_date)]['last_logtime'] = entry.logtime

            logtimes_dict[(employee_id, log_date)]['logs'].append(entry)

        # Serialize the data with total time and late_entry
        serialized_data = []
        for (employee_id, log_date), logtime_data in logtimes_dict.items():
            for log_entry in logtime_data['logs']:
                first_logtime = logtime_data['first_logtime']
                last_logtime = logtime_data['last_logtime']
                total_time = None
                late_entry = None
                early_exit = None

                if first_logtime is not None and last_logtime is not None:
                    time_difference = datetime.combine(date.min, last_logtime) - datetime.combine(date.min, first_logtime)
                    total_seconds = int(time_difference.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                #set total_time to "00:00" if not already set
                if total_time is None:
                    total_time = "00:00"

                if first_logtime is not None and first_logtime > time(8, 15):
                    late_difference = datetime.combine(date.min, first_logtime) - datetime.combine(date.min, time(8, 0))
                    late_seconds = int(late_difference.total_seconds())
                    late_hours, late_remainder = divmod(late_seconds, 3600)
                    late_minutes, late_seconds = divmod(late_remainder, 60)
                    late_entry = f"{late_hours:02d}:{late_minutes:02d}:{late_seconds:02d}"
                
                # Set late_entry to "00:00" if not already set
                if late_entry is None:
                    late_entry = "00:00"

                if early_exit is not None and last_logtime < time(15, 45):
                    early_difference = datetime.combine(date.min, time(16, 0)) - datetime.combine(date.min, last_logtime)
                    early_seconds = int(early_difference.total_seconds())
                    early_hours, early_remainder = divmod(early_seconds, 3600)
                    early_minutes, early_seconds = divmod(early_remainder, 60)
                    early_exit = f"{early_hours:02d}:{early_minutes:02d}:{early_seconds:02d}"

                # Set early_exit to "00:00" if not already set
                if early_exit is None:
                    early_exit = "00:00"

                data = {
                    'id': log_entry.id,
                    'idno': log_entry.idno,
                    'employeeid': log_entry.employeeid,
                    'logdate': log_entry.logdate,
                    'logtime': log_entry.logtime,
                    'direction': log_entry.direction,
                    'shortname': log_entry.shortname,
                    'serialno': log_entry.serialno,
                    'first_logtime': first_logtime,
                    'last_logtime': last_logtime,
                    'total_time': total_time,
                    'late_entry': late_entry,
                    'early_exit': early_exit,
                }
                serialized_data.append(data)

        return Response(serialized_data)







# class LogsView(APIView):
#     @method_decorator(cache_page(60 * 5))  
#     def get(self, request, format=None):
       
#         queryset = Gislogs.objects.order_by('-logdate', 'employeeid')

#         logtimes_dict = {}

#         for entry in queryset:
#             employee_id = entry.employeeid
#             log_date = entry.logdate

#             if (employee_id, log_date) not in logtimes_dict:
#                 if entry.logtime < time(16, 0):
#                     first_logtime = entry.logtime
#                 else:
#                     first_logtime = None

#                 logtimes_dict[(employee_id, log_date)] = {
#                     'first_logtime': first_logtime,
#                     'last_logtime': entry.logtime,
#                     'logs': [],
#                 }
#             else:
#                 logtimes_dict[(employee_id, log_date)]['last_logtime'] = entry.logtime

#             logtimes_dict[(employee_id, log_date)]['logs'].append(entry)

#         serialized_data = []
#         for (employee_id, log_date), logtime_data in logtimes_dict.items():
#             for log_entry in logtime_data['logs']:
#                 first_logtime = logtime_data['first_logtime']
#                 last_logtime = logtime_data['last_logtime']
#                 total_time = None
#                 late_entry = None
#                 early_exit = None

#                 if first_logtime is not None and last_logtime is not None:
#                     time_difference = datetime.combine(date.min, last_logtime) - datetime.combine(date.min, first_logtime)
#                     total_seconds = int(time_difference.total_seconds())
#                     hours, remainder = divmod(total_seconds, 3600)
#                     minutes, seconds = divmod(remainder, 60)
#                     total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

#                 if total_time is None:
#                     total_time = "00:00"

#                 if first_logtime is not None and first_logtime > time(8, 15):
#                     late_difference = datetime.combine(date.min, first_logtime) - datetime.combine(date.min, time(8, 0))
#                     late_seconds = int(late_difference.total_seconds())
#                     late_hours, late_remainder = divmod(late_seconds, 3600)
#                     late_minutes, late_seconds = divmod(late_remainder, 60)
#                     late_entry = f"{late_hours:02d}:{late_minutes:02d}:{late_seconds:02d}"

#                 if late_entry is None:
#                     late_entry = "00:00"

#                 if early_exit is not None and last_logtime < time(15, 45):
#                     early_difference = datetime.combine(date.min, time(16, 0)) - datetime.combine(date.min, last_logtime)
#                     early_seconds = int(early_difference.total_seconds())
#                     early_hours, early_remainder = divmod(early_seconds, 3600)
#                     early_minutes, early_seconds = divmod(early_remainder, 60)
#                     early_exit = f"{early_hours:02d}:{early_minutes:02d}:{early_seconds:02d}"

#                 if early_exit is None:
#                     early_exit = "00:00"

#                 try:
#                     employee_details = detailsOfEmployees.objects.get(employee_id=employee_id)
#                 except detailsOfEmployees.DoesNotExist:
#                     employee_details = None

#                 data = {
#                     'id': log_entry.id,
#                     'idno': log_entry.idno,
#                     'employeeid': log_entry.employeeid,
#                     'logdate': log_entry.logdate,
#                     'logtime': log_entry.logtime,
#                     'direction': log_entry.direction,
#                     'shortname': log_entry.shortname,
#                     'serialno': log_entry.serialno,
#                     'first_logtime': first_logtime,
#                     'last_logtime': last_logtime,
#                     'total_time': total_time,
#                     'late_entry': late_entry,
#                     'early_exit': early_exit,
#                     'device_enroll_id': employee_details.device_enroll_id if employee_details else None,
#                     'employee_name': employee_details.employee_name if employee_details else None,
#                     'company': employee_details.company if employee_details else None,
#                     'location': employee_details.location if employee_details else None,
#                     'job_type': employee_details.job_type if employee_details else None,
#                     'department': employee_details.department if employee_details else None,
#                     'designation': employee_details.designation if employee_details else None,
#                     'category': employee_details.category if employee_details else None,
#                     'status': employee_details.status if employee_details else None,
#                     'date_of_joining': employee_details.date_of_joining if employee_details else None,
#                 }
#                 serialized_data.append(data)

#         return Response(serialized_data)






class LogsView(APIView):
    pagination_class = PageNumberPagination()  # Initialize the pagination class
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, format=None):
        # Get the queryset to calculate the first and last logtimes for each employee on each logdate
        queryset = Gislogs.objects.order_by('-logdate', 'employeeid')

        # Create a dictionary to hold the calculated logtimes for each (employeeid, logdate) pair
        logtimes_dict = {}

        # Loop through the queryset to calculate logtimes
        for entry in queryset:
            employee_id = entry.employeeid
            log_date = entry.logdate

            if (employee_id, log_date) not in logtimes_dict:
                if entry.logtime < time(16, 0):
                    first_logtime = entry.logtime
                else:
                    first_logtime = None

                logtimes_dict[(employee_id, log_date)] = {
                    'first_logtime': first_logtime,
                    'last_logtime': entry.logtime,
                    'logs': [],
                }
            else:
                logtimes_dict[(employee_id, log_date)]['last_logtime'] = entry.logtime

            logtimes_dict[(employee_id, log_date)]['logs'].append(entry)

        # Paginate the queryset
        paginated_queryset = self.pagination_class.paginate_queryset(queryset, request)

        # Serialize the data with total time, late_entry, and early_exit
        serialized_data = []
        for (employee_id, log_date), logtime_data in logtimes_dict.items():
            for log_entry in logtime_data['logs']:
                first_logtime = logtime_data['first_logtime']
                last_logtime = logtime_data['last_logtime']
                total_time = None
                late_entry = None
                early_exit = None

                if first_logtime is not None and last_logtime is not None:
                    time_difference = datetime.combine(date.min, last_logtime) - datetime.combine(date.min, first_logtime)
                    total_seconds = int(time_difference.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Set total_time to "00:00" if not already set
                if total_time is None:
                    total_time = "00:00"

                if first_logtime is not None and first_logtime > time(8, 15):
                    late_difference = datetime.combine(date.min, first_logtime) - datetime.combine(date.min, time(8, 0))
                    late_seconds = int(late_difference.total_seconds())
                    late_hours, late_remainder = divmod(late_seconds, 3600)
                    late_minutes, late_seconds = divmod(late_remainder, 60)
                    late_entry = f"{late_hours:02d}:{late_minutes:02d}:{late_seconds:02d}"

                # Set late_entry to "00:00" if not already set
                if late_entry is None:
                    late_entry = "00:00"

                if early_exit is not None and last_logtime < time(15, 45):
                    early_difference = datetime.combine(date.min, time(16, 0)) - datetime.combine(date.min, last_logtime)
                    early_seconds = int(early_difference.total_seconds())
                    early_hours, early_remainder = divmod(early_seconds, 3600)
                    early_minutes, early_seconds = divmod(early_remainder, 60)
                    early_exit = f"{early_hours:02d}:{early_minutes:02d}:{early_seconds:02d}"

                # Set early_exit to "00:00" if not already set
                if early_exit is None:
                    early_exit = "00:00"

                # Get employee details from detailsOfEmployees model
                try:
                    employee_details = detailsOfEmployees.objects.get(employee_id=employee_id)
                except detailsOfEmployees.DoesNotExist:
                    employee_details = None

                data = {
                    # 'id': log_entry.id,
                    # 'idno': log_entry.idno,
                    'employeeid': log_entry.employeeid,
                    # 'logdate': log_entry.logdate,
                    'logtime': log_entry.logtime,
                    'direction': log_entry.direction,
                    'shortname': log_entry.shortname,
                    'serialno': log_entry.serialno,
                    'first_logtime': first_logtime,
                    'last_logtime': last_logtime,
                    'total_time': total_time,
                    'late_entry': late_entry,
                    'early_exit': early_exit,
                    'device_enroll_id': employee_details.device_enroll_id if employee_details else None,
                    'employee_name': employee_details.employee_name if employee_details else None,
                    'company': employee_details.company if employee_details else None,
                    'location': employee_details.location if employee_details else None,
                    'job_type': employee_details.job_type if employee_details else None,
                    'department': employee_details.department if employee_details else None,
                    'designation': employee_details.designation if employee_details else None,
                    'category': employee_details.category if employee_details else None,
                    'status': employee_details.status if employee_details else None,
                    # 'date_of_joining': employee_details.date_of_joining if employee_details else None,
                }
                serialized_data.append(data)

        response_data = {
            'count': paginated_queryset.count(),
            'next': self.pagination_class.get_next_link(paginated_queryset),
            'previous': self.pagination_class.get_previous_link(paginated_queryset),
            'results': serialized_data,
        }

        return Response(response_data)
    






class Logs2View(APIView):
    pagination_class = CursorPagination()  # Initialize the cursor pagination class
    
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def get(self, request, format=None):
        # Get the queryset to calculate the first and last logtimes for each employee on each logdate
        # queryset = Gislogs.objects.order_by('-logdate', 'employeeid')  # Specify the correct ordering fields
        queryset = Gislogs.objects.all()  # Replace with your specific filtering or retrieval logic

        # Create a dictionary to hold the calculated logtimes for each (employeeid, logdate) pair
        logtimes_dict = {}

        # Loop through the queryset to calculate logtimes
        for entry in queryset:
            employee_id = entry.employeeid
            log_date = entry.logdate

            if (employee_id, log_date) not in logtimes_dict:
                if entry.logtime < time(16, 0):
                    first_logtime = entry.logtime
                else:
                    first_logtime = None

                logtimes_dict[(employee_id, log_date)] = {
                    'first_logtime': first_logtime,
                    'last_logtime': entry.logtime,
                    'logs': [],
                }
            else:
                logtimes_dict[(employee_id, log_date)]['last_logtime'] = entry.logtime

            logtimes_dict[(employee_id, log_date)]['logs'].append(entry)

        # Paginate the queryset
        paginated_queryset = self.pagination_class.paginate_queryset(queryset, request)

        # Serialize the data with total time, late_entry, and early_exit
        serialized_data = []
        for (employee_id, log_date), logtime_data in logtimes_dict.items():
            for log_entry in logtime_data['logs']:
                first_logtime = logtime_data['first_logtime']
                last_logtime = logtime_data['last_logtime']
                total_time = None
                late_entry = None
                early_exit = None

                if first_logtime is not None and last_logtime is not None:
                    time_difference = datetime.combine(date.min, last_logtime) - datetime.combine(date.min, first_logtime)
                    total_seconds = int(time_difference.total_seconds())
                    hours, remainder = divmod(total_seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    total_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

                # Set total_time to "00:00" if not already set
                if total_time is None:
                    total_time = "00:00"

                if first_logtime is not None and first_logtime > time(8, 15):
                    late_difference = datetime.combine(date.min, first_logtime) - datetime.combine(date.min, time(8, 0))
                    late_seconds = int(late_difference.total_seconds())
                    late_hours, late_remainder = divmod(late_seconds, 3600)
                    late_minutes, late_seconds = divmod(late_remainder, 60)
                    late_entry = f"{late_hours:02d}:{late_minutes:02d}:{late_seconds:02d}"

                # Set late_entry to "00:00" if not already set
                if late_entry is None:
                    late_entry = "00:00"

                if early_exit is not None and last_logtime < time(15, 45):
                    early_difference = datetime.combine(date.min, time(16, 0)) - datetime.combine(date.min, last_logtime)
                    early_seconds = int(early_difference.total_seconds())
                    early_hours, early_remainder = divmod(early_seconds, 3600)
                    early_minutes, early_seconds = divmod(early_remainder, 60)
                    early_exit = f"{early_hours:02d}:{early_minutes:02d}:{early_seconds:02d}"

                # Set early_exit to "00:00" if not already set
                if early_exit is None:
                    early_exit = "00:00"

                # Get employee details from detailsOfEmployees model
                try:
                    employee_details = detailsOfEmployees.objects.get(employee_id=employee_id)
                except detailsOfEmployees.DoesNotExist:
                    employee_details = None

                data = {
                    # 'id': log_entry.id,
                    # 'idno': log_entry.idno,
                    'employeeid': log_entry.employeeid,
                    'logdate': log_entry.logdate,
                    'logtime': log_entry.logtime,
                    'direction': log_entry.direction,
                    'shortname': log_entry.shortname,
                    'serialno': log_entry.serialno,
                    # 'first_logtime': first_logtime,
                    # 'last_logtime': last_logtime,
                    'total_time': total_time,
                    'late_entry': late_entry,
                    'early_exit': early_exit,
                    'device_enroll_id': employee_details.device_enroll_id if employee_details else None,
                    'employee_name': employee_details.employee_name if employee_details else None,
                    'company': employee_details.company if employee_details else None,
                    'location': employee_details.location if employee_details else None,
                    'job_type': employee_details.job_type if employee_details else None,
                    'department': employee_details.department if employee_details else None,
                    'designation': employee_details.designation if employee_details else None,
                    'category': employee_details.category if employee_details else None,
                    'status': employee_details.status if employee_details else None,
                    'date_of_joining': employee_details.date_of_joining if employee_details else None,
                }
                serialized_data.append(data)

        response_data = {
            'results': serialized_data,
            'previous': self.pagination_class.get_previous_link(),
            'next': self.pagination_class.get_next_link(),
        }

        return Response(response_data)
    




class CustomCursorPagination(CursorPagination):
    page_size = 100  # Number of items per page
    ordering = '-logdate'  # Ordering for pagination
    max_page_size = 100  # Set a maximum allowed page size

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset.

        If the `page_size` query parameter is provided, it will be used to
        override the default `page_size`.
        """
        self.page_size = self.get_page_size(request)
        return super().paginate_queryset(queryset, request, view)

    def get_page_size(self, request):
        """
        Determine the page size from the request query parameters.
        """
        page_size = request.query_params.get(self.page_size_query_param)
        if page_size is None:
            return self.page_size
        try:
            return min(int(page_size), self.max_page_size)
        except (ValueError, TypeError):
            return self.page_size






    

# @api_view(['GET'])
# def get_combined_logs(request):
#     # Try to get data from cache
#     cached_data = cache.get('combined_logs')
#     if cached_data is not None:
#         return Response(cached_data)

#     # If not in cache, retrieve data and paginate
#     gislogs_queryset = Gislogs.objects.all()  # Modify this queryset as needed
#     paginator = CustomCursorPagination()
#     # paginator = CursorPagination()
#     paginated_queryset = paginator.paginate_queryset(gislogs_queryset, request)

#     serializer = CombinedLogsSerializer(paginated_queryset, many=True)

#     # Store data in cache for 5 minutes
#     cache.set('combined_logs', serializer.data, 300)

#     return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
def get_combined_logs(request):
    # Try to get data from cache
    # cached_data = cache.get('combined_logs')
    # if cached_data is not None:
    #     return Response(cached_data)

    # If not in cache, retrieve data and paginate
    # gislogs_queryset = Gislogs.objects.all()  # Modify this queryset as needed
    gislogs_queryset = Gislogs.objects.order_by('-logdate', 'employeeid')  # Order the queryset
    detailsOfEmployees_queryset = detailsOfEmployees.objects.all()  # Modify this queryset as needed
    paginator = PageNumberPagination()

    # Retrieve the `page_size` from the query parameters
    page_size = request.query_params.get('page_size')
    if page_size:
        paginator.page_size = int(page_size)

    paginated_queryset = paginator.paginate_queryset(gislogs_queryset, request)

    serializer = CombinedLogsSerializer(paginated_queryset, many=True)

    # Store data in cache for 5 minutes
    # cache.set('combined_logs', serializer.data, 300)

    return paginator.get_paginated_response(serializer.data)




# @api_view(['GET'])
# def get_combined_logs2(request):
#     # Try to get data from cache
#     # cached_data = cache.get('combined_logs')
#     # if cached_data is not None:
#     #     return Response(cached_data)

#     # If not in cache, retrieve data and paginate
#     gislogs_queryset = Gislogs.objects.order_by('-logdate', 'employeeid')  # Order the queryset
#     detailsOfEmployees_queryset = detailsOfEmployees.objects.all()  # Modify this queryset as needed
#     paginator = PageNumberPagination()

#     # Retrieve the `page_size` from the query parameters
#     page_size = request.query_params.get('page_size')
#     if page_size:
#         paginator.page_size = int(page_size)

#     paginated_queryset = paginator.paginate_queryset(gislogs_queryset, request)

#     serializer = CombinedLogs2Serializer(paginated_queryset, many=True)

#     # Store data in cache for 5 minutes
#     # cache.set('combined_logs', serializer.data, 300)

#     return paginator.get_paginated_response(serializer.data)








# @api_view(['GET'])
# def get_combined_logs(request):
#     gislogs_queryset = Gislogs.objects.all()
#     employee_queryset = detailsOfEmployees.objects.all()

#     # Handle search parameter
#     search_param = request.query_params.get('search')
#     if search_param:
#         employee_queryset = employee_queryset.filter(
#             Q(employee_name__icontains=search_param) |
#             Q(employee_id__icontains=search_param)  # Include employee_id in the search
#         )

#     # Handle filter parameters (example: location)
#     location_filter = request.query_params.get('location')
#     if location_filter:
#         gislogs_queryset = gislogs_queryset.filter(employee__location=location_filter)

#     # Handle logdate filter parameter
#     logdate_filter = request.query_params.get('logdate')
#     if logdate_filter:
#         gislogs_queryset = gislogs_queryset.filter(logdate=logdate_filter)

#     # Handle logtime filter parameter
#     logtime = request.query_params.get('logtime')
#     if logtime:
#         if logtime == None :
#             gislogs_queryset = gislogs_queryset.filter(logtime__isnull=True)
#         elif ':' in logtime:  # Check if the filter contains a colon (':' indicates a specific time)
#             specific_time = datetime.strptime(logtime, '%H:%M').time()
#             gislogs_queryset = gislogs_queryset.filter(logtime=specific_time)
#         else:
#             # Split the logtime_filter into start and end times for time range
#             start_time, end_time = logtime.split('-')
#             start_time = datetime.strptime(start_time, '%H:%M').time()
#             end_time = datetime.strptime(end_time, '%H:%M').time()
#             gislogs_queryset = gislogs_queryset.filter(logtime__range=[start_time, end_time])


#     # Handle date range filter parameters
#     start_date = request.query_params.get('start_date')
#     end_date = request.query_params.get('end_date')
#     if start_date and end_date:
#         gislogs_queryset = gislogs_queryset.filter(logdate__range=[start_date, end_date])

#     # Consolidated handling of shift_status filter
#     shift_status = request.query_params.get('shift_status')
#     valid_shift_statuses = ['P', 'P/A', 'A/P', 'A']
#     if shift_status in valid_shift_statuses:
#         gislogs_queryset = gislogs_queryset.filter(shift_status=shift_status)

#     # Consolidated handling of time filters (first_logtime and logtime)
#     # time_filter = request.query_params.get('time')
#     # if time_filter:
#     #     gislogs_queryset = apply_time_filter(gislogs_queryset, time_filter)


#     # Handle sorting parameter
#     ordering = request.query_params.get('ordering', '-logdate')
#     gislogs_queryset = gislogs_queryset.order_by(ordering)

#     paginator = PageNumberPagination()

#     # Retrieve the `page_size` from the query parameters
#     page_size = request.query_params.get('page_size')
#     if page_size:
#         paginator.page_size = int(page_size)

#     paginated_queryset = paginator.paginate_queryset(gislogs_queryset, request)

#     serializer = CombinedLogsSerializer(paginated_queryset, many=True)

#     return paginator.get_paginated_response(serializer.data)


    




class CombinedAutocompleteViewSet(viewsets.ViewSet):
    def list(self, request):
        search_term = request.query_params.get('term')
        if search_term:
            gislogs_suggestions = Gislogs.objects.filter(
                Q(shortname__icontains=search_term) |
                Q(serialno__icontains=search_term)
            )[:10]
            gislogs_suggestions = list(gislogs_suggestions)

            employee_suggestions = detailsOfEmployees.objects.filter(
                Q(employee_name__icontains=search_term) 
                # Q(employee_id__icontains=search_term)
            )[:10]
            employee_suggestions = list(employee_suggestions)

            suggestions = []

            for item in gislogs_suggestions:
                value = f"{item.shortname} - {item.serialno}"
                suggestions.append({'id': item.id, 'value': value})

            for item in employee_suggestions:
                value = f"{item.employee_name}"
                suggestions.append({'id': item.id, 'value': value})

            return Response(suggestions)
        return Response([])
    



class DetailsOfEmployeesCRUDView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = detailsOfEmployees.objects.order_by('employee_id')
    serializer_class = detailsOfEmployeesSerializer
    pagination_class = PageNumberPagination  # You can use your custom pagination if needed

    def list(self, request, *args, **kwargs):
        # Retrieve the `page_size` from the query parameters
        page_size = request.query_params.get('page_size')
        if page_size:
            self.pagination_class.page_size = int(page_size)
        return super().list(request, *args, **kwargs)











# class EmployeeLogAPIView(generics.ListAPIView):
#     queryset = detailsOfEmployees.objects.annotate(logdate=F('gislogs__logdate')).order_by('-logdate')
#     serializer_class = detailsOfEmployeesSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         # Get the page size from the query parameter
#         page_size = self.request.query_params.get('page_size')

#         # Create a new instance of the pagination class
#         paginator = self.pagination_class()

#         # Apply the custom page size if provided in the query parameter
#         if page_size:
#             paginator.page_size = int(page_size)

#         # Get the paginated queryset using the adjusted page size
#         paginated_queryset = paginator.paginate_queryset(self.queryset, self.request)

#         return paginated_queryset

    


class CombinedDetails(APIView):
    def get(self, request, format=None):
        # Get all distinct log dates
        log_dates = Gislogs.objects.values_list('logdate', flat=True).distinct()

        # Get all EmployeeData records
        employees = detailsOfEmployees.objects.all()

        combined_data = []

        for employee in employees:
            employee_data = {
                "employee_id": employee.employee_id,
                "device_enroll_id": employee.device_enroll_id,
                "employee_name": employee.employee_name,
                "company": employee.company,
                "location": employee.location,
                "job_type": employee.job_type,
                "department": employee.department,
                "designation": employee.designation,
                "category": employee.category,
                "status": employee.status,
                "date_of_joining": employee.date_of_joining,
            }

            log_entries = []

            for log_date in log_dates:
                logs_entry = Gislogs.objects.filter(employeeid=employee.employee_id, logdate=log_date).first()

                if not logs_entry:
                    # Employee is absent on this logdate
                    log_entry = {
                        "logdate": log_date,
                        "logtime": None,
                        "direction": None,
                        "shortname": None,
                        "serialno": None,
                    }
                else:
                    # Employee is present on this logdate
                    log_entry = {
                        "logdate": log_date,
                        "logtime": logs_entry.logtime,
                        "direction": logs_entry.direction,
                        "shortname": logs_entry.shortname,
                        "serialno": logs_entry.serialno,
                    }

                log_entries.append(log_entry)

            combined_entry = {
                **employee_data,
                "logdata": log_entries,
            }

            combined_data.append(combined_entry)

        paginator = PageNumberPagination()
        page_size = request.query_params.get('page_size', 10)
        paginator.page_size = page_size

        result_page = paginator.paginate_queryset(combined_data, request)
        serializer = CombinedDetailsSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)