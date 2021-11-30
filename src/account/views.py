from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls.base import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, ListView
from .forms import LoginForm, CustomUserCreation, DisableUser
from .mixins import IsManagerMixin

# Create your views here.
class Login(View):
    template_name = 'account/login.html'
    form_class = LoginForm
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)

        form = self.form_class
        context = {
            'form': form,
        }

        return render(self.request, self.template_name,context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username = cd['username'],
                password = cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('event:event_list')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.warning(request, 'Incorrect username/password')
                return HttpResponse('Invalid Login')

        return render(request, self.template_name, {'form':form})

class UserList(LoginRequiredMixin, IsManagerMixin, ListView):
    template_name = 'account/user_list.html'
    queryset = get_user_model().objects.all()

class CreateUser(LoginRequiredMixin, IsManagerMixin, CreateView):
    template_name = 'account/create_user.html'
    model = get_user_model()
    form_class = CustomUserCreation
    success_url = '/account/'

class UserDetail(LoginRequiredMixin, IsManagerMixin, DetailView):
    template_name = 'account/user_detail.html'
    user = get_user_model()
    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(self.user, id = id_)

class DisableUser(LoginRequiredMixin, IsManagerMixin, UpdateView):
    template_name = 'account/disable_user.html'
    model = get_user_model()
    form_class = DisableUser

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(self.model, id=id_)

    def get_success_url(self):
        return reverse_lazy('account:user_detail', kwargs={'id': self.object.id})


def Logout_view(request):
    logout(request)
    return redirect('account:login')