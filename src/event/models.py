from django.conf import settings
from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from supplier.models import Company

import os

# Create your models here.
class Event(models.Model):
    name = models.CharField(blank=False, null=False, max_length=150)
    slug = models.SlugField(unique=True, max_length=150)
    date = models.DateField(blank=False, null=False)
    is_active = models.BooleanField(default=True)
    bib_required = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    suppliers = models.ManyToManyField(Company, related_name="supplies_for_event")
    logistic_staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="authorised_for_event")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event:dashboard', kwargs={'slug': self.slug})
        # return reverse('event:event_list')

def createSlug(instance, new_slug=None):
    slug = slugify(instance.name)
    if new_slug is not None:
        slug = new_slug
    qs = Event.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return createSlug(instance, new_slug=new_slug)
    return slug

def pre_save_event_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = createSlug(instance)

pre_save.connect(pre_save_event_receiver, sender=Event)

class Worker(models.Model):
    payroll_id = models.CharField(max_length=7, null=False, blank=False, unique=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(blank=False, null=False)
    employer = models.ForeignKey(Company, limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    working_at = models.ForeignKey(Event, limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    sia_no = models.CharField(max_length=19, blank=True, null=True)
    sia_exp = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    dateEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f"{self.first_name}_{self.last_name}"

    def get_absolute_url(self):
        return reverse('event:worker_detail', kwargs={'slug':self.working_at.slug,'id':self.id })

    def get_accreditation(self):
        result = self.accredit_set.get(worker = self)
        return result

    @property
    def is_approved(self):
        result = self.accredit_set.get(worker=self)
        return result.is_complete

    @property
    def when_approved(self):
        result = self.accredit_set.get(worker=self)
        return result.dateEntered

    @property
    def approved_by(self):
        result = self.accredit_set.get(worker=self)
        return result.approved_by

    @property
    def can_be_approved(self):

        is_approved = False
        try:
            is_approved =  self.accredit_set.get(worker=self).is_complete
        except Accredit.DoesNotExist:
            pass
        if self.working_at.is_active and not is_approved:
            return True
        return False

        

class BulkInsert(models.Model):

    event = models.ForeignKey(Event, on_delete = models.CASCADE)
    company = models.ForeignKey(Company, on_delete = models.CASCADE,limit_choices_to={'is_active': True},)
    staffCSVFile = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, null=True)
    dateEntered = models.DateTimeField(auto_now=False,auto_now_add=True)

    def get_absolute_url(self):
        return reverse('event:worker_bulk_create', kwargs={'slug': self.event.slug})


class Accredit(models.Model):
    TRANSPORT_CHOICES = (
        (None, 'Please select transport'),
        ('Company', 'Company Provided Transport'),
        ('Public','Public Transport'),
        ('Private', 'Private Transport'),
        )
    
    APPROVED_ID = (
        (None, 'Please Select ID'),
        ('SIA', 'SIA Licence'),
        ('Driver', 'Drivers Licence'),
        ('Passport', 'Passport'),
        ('StaffIDCard','Approved Staff ID Card'),
        ('PASS', 'Pass Scheme Card'),
        )

    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    firstIdChecked = models.CharField(max_length=50,choices=APPROVED_ID)
    secondIdChecked = models.CharField(max_length=50, choices=APPROVED_ID)
    camping = models.BooleanField(null=True, blank=True)
    transport_home = models.CharField(max_length=50, choices=TRANSPORT_CHOICES)
    role = models.ForeignKey('Role', on_delete=models.DO_NOTHING)
    tent = models.ForeignKey('Tent', on_delete=models.DO_NOTHING, null=True)
    wristband = models.ForeignKey('Wristband', on_delete=models.DO_NOTHING)
    bib = models.ForeignKey('Bib', on_delete=models.SET_NULL, null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    dateEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    dateUpdated = models.DateTimeField(auto_now=True, auto_now_add=False)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return f" Worker {self.worker}, tent {self.tent}, wristband {self.wristband}"

    @property
    def get_image_url(self):
        image =  self.workerimage_set.get(accredit=self)
        return image.image.url

class Role(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.name

class Tent(models.Model):
    tent_tag = models.CharField(max_length=20, null=True, blank=True)
    tent_tag_colour = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    dateEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    # accredit = models.ForeignKey(Accredit, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tent tag {self.tent_tag} with colour {self.tent_tag_colour}"

class Wristband(models.Model):
    wristband_no = models.CharField(max_length=15, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    dateEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    # accredit = models.ForeignKey(Accredit, on_delete=models.CASCADE)

    def __str__(self):
        return self.wristband_no

class Bib(models.Model):
    bib_no = models.CharField(max_length=15, null=False, blank=False)
    bib_colour = models.CharField(max_length=15, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    dateEntered = models.DateTimeField(auto_now=False, auto_now_add=True)
    # accredit = models.ForeignKey(Accredit, on_delete=models.CASCADE)

    def __str__(self):
        return f"Bib no {self.bib_no} with colour {self.bib_colour}"

def upload_location(instance, filename):
    return f"photo/{filename}"

class WorkerImage(models.Model):
    
    image = models.ImageField(upload_to=upload_location, default=os.path.join(settings.MEDIA_ROOT, 'avatar.png'))
    is_active = models.BooleanField(default=True)
    accredit = models.ForeignKey(Accredit, on_delete=models.CASCADE)
