from django.urls import path
from .views import CompanyList, CompanyCreate, CompanyDisable

app_name = 'supplier'

urlpatterns = [
    path('', CompanyList.as_view(), name='company_list'),
    path('create/', CompanyCreate.as_view(), name='company_create'),
    path('<int:id>/edit/', CompanyDisable.as_view(), name='company_disable'),   
]