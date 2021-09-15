from django.db.models import fields
from django.forms import forms, widgets
from django.contrib.auth.models import User
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = '__all__'
        widgets = {'date_added': DateInput()}


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['user', 'category', 'name', 'rep_name', 'designation', 'phone', 'email', 'num_of_site', 'date_created']
        ordering = ['date_created']
        widgets = {'date_created': DateInput()}
        
        """
        widgets = {
            'user': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'rep_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'num_of_site': forms.TextInput(attrs={'class': 'form-control'}),    
        }

        """


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'




class PageOneForm(forms.ModelForm):

    class Meta:
        model = PageOne
        fields = '__all__'
        widgets = {'date': DateInput()}



class PageTwoForm(forms.ModelForm):
    class Meta:
        model = PageTwo
        fields = '__all__'
        


class PageThreeForm(forms.ModelForm):
    class Meta:
        model = PageThree
        fields = '__all__'


class PageFourForm(forms.ModelForm):
    class Meta:
        model = PageFour
        fields = '__all__'


class PageFiveForm(forms.ModelForm):
    class Meta:
        model = PageFive
        fields = '__all__'


class PageSixForm(forms.ModelForm):
    class Meta:
        model = PageSix
        fields = '__all__'


class PageSevenForm(forms.ModelForm):
    class Meta:
        model = PageSeven
        fields = '__all__'


class FillingStationPageOneForm(forms.ModelForm):
    class Meta:
        model = FillingStationPageOne
        fields = '__all__'


class FillingStationPageTwoForm(forms.ModelForm):
    class Meta:
        model = FillingStationPageTwo
        fields = '__all__'


class CommercialIndustryPageOneForm(forms.ModelForm):
    class Meta:
        model = CommercialIndustryPageOne
        fields = '__all__'


class CommercialIndustryPageTwoForm(forms.ModelForm):
    class Meta:
        model = CommercialIndustryPageTwo
        fields = '__all__'

