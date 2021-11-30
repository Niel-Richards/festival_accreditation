from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from .forms import CreateCompanyForm
from .models import Company
from account.mixins import IsManagerMixin
#Company Views below

class CompanyList(LoginRequiredMixin, IsManagerMixin, ListView):
    template_name = 'management/company_list.html'
    queryset = Company.objects.all()

class CompanyCreate(LoginRequiredMixin, IsManagerMixin, CreateView):
    template_name = 'management/company_create.html'
    form_class = CreateCompanyForm
    success_url = '/company/'
    model = Company

class CompanyDisable(LoginRequiredMixin, IsManagerMixin, UpdateView):
    template_name = 'management/company_disable.html'
    success_url = '/company/'
    model = Company
    fields = ['is_active']

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Company, id=id_)

    def form_valid(self, form):
        if self.request.POST.get('toggle') == 'enable':
            form.instance.is_active = True
        else:
            form.instance.is_active = False
        return super().form_valid(form)