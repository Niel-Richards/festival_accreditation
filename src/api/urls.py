from django.urls import path
from .views import Worker_List, CheckStaffPayrollID

app_name = 'api'

urlpatterns = [
    path('worker/<int:event_id>/<str:name>', Worker_List, name='worker_list'),
    path('worker/payroll/<str:payroll_id>/', CheckStaffPayrollID, name='worker_payroll_id'),
]