from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from event.forms import AccreditForm, BibForm, BulkCreateWorkerForm, CreateWorker, EventAssignSuppliersForm, EventForm, EventAssignLogisticsUserForm, WristBandForm
from django.db.models import F, Count, When, Value, Case, Sum
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView
from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from .models import Event, Worker, Accredit, Tent, WorkerImage, Role
from account.mixins import IsManagerMixin, IsAuthorisedMixin

import base64
import datetime

class EventCreateView(LoginRequiredMixin, IsManagerMixin, CreateView):
    template_name = 'event/create_event.html'
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event:dashboard', kwargs={'slug': self.object.slug})    

class EventListView(LoginRequiredMixin, ListView):
    template_name = 'event/event_list.html'
    queryset = Event.objects.all()

class EventDetailView(LoginRequiredMixin,IsAuthorisedMixin, DetailView):
    template_name = 'event/dashboard.html'
    model = Event

    def get_object(self):
        slug_ = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.get_object()
        context['accredit_by_company_sum'] = Accredit.objects.filter(worker__working_at = event.id).values(name=F('worker__employer__name')).annotate(num_workers=Count('id'))
        context['accredit_by_role_sum'] = Role.objects.all().annotate(num_workers=Sum(Case(When(accredit__worker__working_at = event.id, then=Value(1)),default=Value(0),)))
        context['summary'] = Worker.objects.filter(working_at=event.id).values(name=F('employer__name')).annotate(worker_count=Count('id')).annotate(workers_accreditted=Count('accredit__id'))
        return context

class EventCloseView(LoginRequiredMixin, IsManagerMixin, UpdateView):
    template_name = 'event/close_event.html'
    model = Event
    fields = ['is_active']
    
    def get_object(self):
        slug_ = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug_)

    def get_success_url(self):
        return reverse_lazy('event:dashboard', kwargs={'slug': self.object.slug})

class EventAssignSupplier(LoginRequiredMixin, IsManagerMixin, UpdateView):
    template_name = 'event/assign_company.html'
    model = Event
    form_class = EventAssignSuppliersForm

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Event, slug=slug_)

    def get_success_url(self):
        return reverse_lazy('event:dashboard', kwargs={'slug': self.object.slug})

class EventAssignLogisticsStaff(LoginRequiredMixin, IsManagerMixin, UpdateView):
    template_name = 'event/assign_logistics_staff.html'
    model = Event
    form_class = EventAssignLogisticsUserForm

    def get_object(self):
        slug_ = self.kwargs.get("slug")
        return get_object_or_404(Event, slug=slug_)

    def get_success_url(self):
        return reverse_lazy('event:dashboard', kwargs={'slug': self.object.slug})

class WorkerSearch(LoginRequiredMixin, View):

    template_name = 'worker/worker_search.html'

    def get_object(self):
        slug_ = self.kwargs.get('slug')
        return get_object_or_404(Event, slug=slug_)

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        context = {
            'object':object,
        }
        return render(request, self.template_name, context)

class WorkerCreate(LoginRequiredMixin, CreateView):
    template_name = 'worker/worker_create.html'
    model = Worker
    form_class = CreateWorker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(slug=self.kwargs.get('slug'))
        context['object'] = event
        return context

    def get_form_kwargs(self):
        kwargs = super(WorkerCreate, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs.get('slug')
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        event = Event.objects.get(slug=self.kwargs.get('slug'))
        form.instance.working_at = event
        return super().form_valid(form)

class WorkerBulkCreate(LoginRequiredMixin, IsManagerMixin, CreateView):
    template_name = 'worker/bulk_worker_upload.html'
    form_class = BulkCreateWorkerForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(slug=self.kwargs.get('slug'))
        context['object'] = event
        return context

    def get_form_kwargs(self):
        kwargs = super(WorkerBulkCreate, self).get_form_kwargs()
        kwargs['slug'] = self.kwargs.get('slug')
        return kwargs

    def form_valid(self, form):
        form.instance.uploaded_by_user = self.request.user
        form.instance.event = Event.objects.get(slug=self.kwargs.get('slug'))
        messages.success(self.request, 'File uploaded')
        return super().form_valid(form)


class WorkerDetail(LoginRequiredMixin, DetailView):
    template_name = 'worker/worker_details.html'
    model = Worker

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Worker, id=id_)

class WorkerUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'worker/worker_edit.html'
    model = Worker
    form_class = CreateWorker

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Worker, id=id_)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['slug'] = self.kwargs.get('slug')
        return kwargs

    def get_success_url(self):
        return reverse_lazy('event:worker_detail', kwargs={'id': self.object.id, 'slug': self.object.working_at.slug})

class WorkerAccredit(LoginRequiredMixin, View):
    template_name = 'worker/worker_accredit.html'
    acccreditForm = AccreditForm
    wristbandForm = WristBandForm
    bibForm = BibForm

    def get_time(self):
        time_now = datetime.datetime.now()
        return time_now.strftime('%I%M')

    def get_object(self):
        id_ = self.kwargs.get('id')
        return get_object_or_404(Worker, id=id_)

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        try: 
            if object.is_approved:
                messages.warning(request, 'Staff member already accredited')
                return redirect(object.get_absolute_url())
        except Accredit.DoesNotExist:
            pass

        bib = None
        if object.working_at.bib_required:
            bib = self.bibForm
        context = {
            'object': object,
            'accredit': self.acccreditForm,
            'wristband': self.wristbandForm,
            'bib': bib,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        accredit = self.acccreditForm(request.POST)
        wristband = self.wristbandForm(request.POST)

        if accredit.is_valid() and wristband.is_valid():
            new_accredit = accredit.save(commit=False)
            new_wristband = wristband.save(commit=False)
            
            # process forms
            new_wristband.save()
            if accredit.cleaned_data['camping']:
                new_tent = Tent(tent_tag = accredit.cleaned_data['tent_tag'], tent_tag_colour = accredit.cleaned_data['tent_tag_colour'])
                new_tent.save()
                new_accredit.tent = new_tent

            new_accredit.approved_by = request.user
            new_accredit.worker = self.get_object()
            new_accredit.wristband = new_wristband

            new_accredit.is_complete = True
            new_accredit.save()

            photo = accredit.cleaned_data['mugshot']
            image_data = base64.b64decode(photo)
            new_worker_image = WorkerImage()
            new_worker_image.image.save(f"{new_accredit.worker}{self.get_time()}.png", ContentFile(image_data), save=False)
            new_worker_image.accredit = new_accredit
            new_worker_image.save()

            # process bib and or images then add to accredit

            return redirect(self.get_object().get_absolute_url())
        return render(request,self.template_name,{'accredit':accredit, 'wristband': wristband, 'object':self.get_object()})


class ManagerOptions(LoginRequiredMixin, TemplateView):
    template_name = 'management/manager_options.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name,{})



