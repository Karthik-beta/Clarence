from django.urls import re_path, path
from reportapp import views
from reportapp.views import (
    EmployeeDetailView,
    AllEmployeesView,
    EmployeePresenceView,
    AttendanceStatisticsAPIView,
    AttendanceStatistics2APIView,
    FirstLastLogTimeView,
    LogsView,
    Logs2View,
    get_combined_logs,
    CombinedAutocompleteViewSet,
    DetailsOfEmployeesCRUDView,
    # EmployeeLogAPIView,
    CombinedDetails,
)


combined_autocomplete_view = CombinedAutocompleteViewSet.as_view({'get': 'list'})




urlpatterns = [

    re_path(r'^rawData/$', views.rawDataApi),
    re_path(r'^rawData/([0-9]+)$', views.rawDataApi),

    re_path(r'^processedData/$', views.processedDataApi),
    re_path(r'^processedData/([0-9]+)$', views.processedDataApi),

    path('employee/<int:employee_id>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/', views.AllEmployeesView.as_view(), name='all-employees'),
    # re_path(r'^employee/$', views.AllEmployeesView.as_view(), name='all-employees'),

    re_path(r'^employee_presence/$', EmployeePresenceView.as_view()),

    re_path(r'^AttendanceStatistics/$', AttendanceStatisticsAPIView.as_view()),

    re_path(r'^AttendanceStatistics2/$', AttendanceStatistics2APIView.as_view()),

    re_path(r'^FirstLastLogTime/$', FirstLastLogTimeView.as_view()),

    re_path(r'^EmployeeLogs/$', LogsView.as_view(), name='employee-logs'),

    re_path(r'^EmployeeLogs2/$', Logs2View.as_view(), name='employee-logs2'),

    # path('api/combined-logs/', get_combined_logs.as_view(), name='combined-logs'),
    # re_path(r'^combined-logs/$', get_combined_logs, name='combined-logs'),

    # re_path(r'^combined-logs/$', get_combined_logs, name='combined-logs'),

    re_path(r'^combined-logs/$', CombinedDetails.as_view(), name='combined-logs'),

    # path('api/combined-logs/', get_combined_logs, name='get_combined_logs'),

    re_path(r'^combined-autocomplete/$', combined_autocomplete_view, name='combined-autocomplete'),

    re_path(r'^employeecrud/$', DetailsOfEmployeesCRUDView.as_view()),

]