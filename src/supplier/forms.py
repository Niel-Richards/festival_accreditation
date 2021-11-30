from django import forms
from django.core.exceptions import ValidationError
from .models import Company

class CreateCompanyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CreateCompanyForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['autofocus'] = True


    class Meta:
        model = Company
        fields = ['name',]
        labels = {
            'name': ('Company Name'),
        }
