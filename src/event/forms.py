from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Accredit, BulkInsert, Event, Worker, Wristband, Bib, Tent, Role
from supplier.models import Company


class EventForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control'
        self.fields['bib_required'].widget.attrs['class'] = 'form-check-input'

    class Meta:
        model = Event
        fields = ['name', 'date', 'bib_required']
        labels = {
            'name': ('Event Name'),
            'date': ('Date Of Event'),
            'bib_required': ('Are Bibs Required')
        }

class CustomMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return f"{obj.name}"

class CustomUserMMCF(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return f"{obj.get_full_name()}"

class EventAssignSuppliersForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['suppliers']

    suppliers = CustomMMCF(
        queryset= Company.objects.all(),
        widget = forms.CheckboxSelectMultiple(),
        initial = 0
    )
        
    def __init__(self, *args, **kwargs):
        super(EventAssignSuppliersForm, self).__init__(*args,**kwargs)
        self.fields['suppliers'].queryset = Company.objects.all()


class EventAssignLogisticsUserForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['logistic_staff']

    logistic_staff = CustomUserMMCF(
        queryset= get_user_model().objects.all(),
        widget = forms.CheckboxSelectMultiple,
        initial = 0
    )

class CreateWorker(forms.ModelForm):
    DATE_PLACEHOLDER = 'DD/MM/YYYY'

    def __init__(self, slug, *args, **kwargs):
        super(CreateWorker, self).__init__(*args, **kwargs)
        self.fields['payroll_id'].widget.attrs['class'] = 'form-control uppercase'
        self.fields['payroll_id'].widget.attrs['placeholder'] = 'ABC0000'
        self.fields['payroll_id'].widget.attrs['autofocus'] = True
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_birth'].widget.attrs['placeholder'] = self.DATE_PLACEHOLDER
        self.fields['employer'].widget.attrs['class'] = 'form-select'
        self.fields['employer'].queryset = Company.objects.filter(is_active = True, supplies_for_event__slug =  slug)
        self.fields['sia_no'].widget.attrs['class'] = 'form-control'
        self.fields['sia_no'].widget.attrs['placeholder'] = '0000-0000-0000-0000'
        self.fields['sia_exp'].widget.attrs['class'] = 'form-control'
        self.fields['sia_exp'].widget.attrs['placeholder'] = self.DATE_PLACEHOLDER

    class Meta:
        model = Worker
        exclude = ['created_by','working_at',]
        labels = {
                'payroll_id': ('ID No#'),
                'first_name': ('First Name'),
                'last_name': ('Last Name'),
                'date_of_birth': ('Date Of Birth'),
                'employer': ('Employer'),
                'sia_no': ('SIA No#'),
                'sia_exp': ('SIA Expiry Date'),
        }

class BulkCreateWorkerForm(forms.ModelForm):

    class Meta:
        model = BulkInsert
        fields = ['company', 'staffCSVFile',]
        labels = {
                'company': ('Company'),
                'staffCSVFile': ('Select CSV File'),
        }
    
    def __init__(self, slug, *args, **kwargs):
        super(BulkCreateWorkerForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(is_active = True, supplies_for_event__slug =  slug)
        self.fields['company'].widget.attrs['class'] = 'form-select'
        self.fields['staffCSVFile'].widget.attrs['class'] = 'form-control'

# Start of accreditation

class RoleForm(forms.ModelForm):

    class Meta:
        model = Role
        fields = '__all__'
        labels = {
            'name': ('Name'),
        }

class TentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(TentForm, self).__init__(*args, **kwargs)
        self.fields['tent_tag'].widget.attrs['class'] = 'form-control'
        self.fields['tent_tag_colour'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Tent
        fields = ['tent_tag', 'tent_tag_colour']
        labels = {
            'tent_tag': ('Tent Tag'),
            'tent_tag_colour': ('Tent Tag Colour'),
        }

class WristBandForm(forms.ModelForm):

    class Meta:
        model = Wristband
        fields = ['wristband_no']
        labels = {
            'wristband_no': ('Wristband No'),
        }

    def __init__(self, *args, **kwargs):
        super(WristBandForm, self).__init__(*args, **kwargs)
        self.fields['wristband_no'].widget.attrs['class'] = 'form-control'
        

class BibForm(forms.ModelForm):

    class Meta:
        model = Bib
        fields = ['bib_no', 'bib_colour']
        labels = {
            'bib_no': ('Bib No'),
            'bib_colour':  ('Bib Colour'),
        }

class AccreditForm(forms.ModelForm):

    tent_tag = forms.CharField(max_length=20, label='Tent Tag', required=False)
    tent_tag_colour = forms.CharField(max_length=20, label='Tent Tag Colour', required=False)
    mugshot = forms.CharField(label="")
    
    def __init__(self, *args, **kwargs):
        super(AccreditForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['class'] = 'form-select'
        self.fields['firstIdChecked'].widget.attrs['class'] = 'form-select'
        self.fields['secondIdChecked'].widget.attrs['class'] = 'form-select'
        self.fields['camping'].widget.attrs['class'] = 'form-select'
        self.fields['transport_home'].widget.attrs['class'] = 'form-select'
        self.fields['tent_tag'].widget.attrs['class'] = 'form-control'
        self.fields['tent_tag_colour'].widget.attrs['class'] = 'form-control'
        self.fields['mugshot'].widget.attrs['hidden'] = True

    def clean(self):
        first = self.cleaned_data['firstIdChecked']
        second = self.cleaned_data['secondIdChecked']

        if second == first:
            raise ValidationError('Two forms of ID need to be checked!')

        camping = self.cleaned_data['camping']
        tent_tag = self.cleaned_data['tent_tag']
        tent_tag_colour = self.cleaned_data['tent_tag_colour']

        if camping:
            if ((tent_tag == "") or (tent_tag_colour == "")):
                raise ValidationError('All camping details are required')


    class Meta:
        model = Accredit
        fields = ['role', 'firstIdChecked', 'secondIdChecked', 'camping', 'transport_home']
        labels = {
            'role': ('Role'),
            'firstIdChecked': ('ID Check 1'),
            'secondIdChecked': ('ID Check 2'),
            'camping': ('Are you Camping'),
            'transport_home': ('How are you getting home'),
        }

    
# end of accreditation
