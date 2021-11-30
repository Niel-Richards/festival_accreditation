from event.models import Worker
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
def Worker_List(request,name):
    result = {}
    if name is not None:
        query = Worker.objects.filter(last_name__icontains=name)
        for count, worker in enumerate(query):
            result[count] = {
                'id': worker.id,
                'first_name': worker.first_name,
                'last_name': worker.last_name,
                'date_of_birth': worker.date_of_birth,
                'employer': worker.employer.name,
                'url': worker.get_absolute_url(),
            }
    return JsonResponse(result)

def CheckStaffPayrollID(request, payroll_id):
    result = {'exists':False}
    if payroll_id is not None:
        query = Worker.objects.filter(payroll_id = payroll_id)
        result['exists'] = query.exists()
    return JsonResponse(result)
    
