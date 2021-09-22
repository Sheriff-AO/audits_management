import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView
from formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import *
from .forms import *

@login_required
def index(request):
    return render(request, 'audits/index.html')


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    context_object_name = 'clients'


@login_required
def clientDetail(request, pk):
    client = Client.objects.get(id=pk)
    sites = Site.objects.filter(client=client)
    total_site = Site.objects.filter(client=client).count()
    context = {
        'client': client,
        'sites': sites,
        'total_site': total_site
    }
    return render(request, 'audits/clientDetail.html', context)


class SiteListView(LoginRequiredMixin, ListView):
    model = Site
    template_name = 'audits/site.html'
    context_object_name = 'sites'
    ordering = ['-date_added']


class AllVendorListView(ListView):
    model = Vendor
    template_name = 'audits/all_vendor.html'
    context_object_name = 'vendors'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['vendors'] = context['vendors'].all()
        else:
            context['vendors'] = context['vendors'].filter(user=self.request.user) 
        
        #context['count'] = context['vendors'].filter(complete=True).count()
        return context
   

# def vendorList(request):
#     vendors = Vendor.objects.filter(user=request.user)
#     context = {
#         'vendors': vendors
#     }
#     return render(request, 'audits/vendor_list.html', context)


@login_required
def createSite(request):
    form = SiteForm()
    if request.method == 'POST':
        print('Printing POST:', request.POST)
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Site successfully created!")
            return redirect('audits:site')
        messages.error(request, "There was an Error while filling the form, Please re-check!")

    context = {
        'form': form
    }
    return render(request, 'audits/site_form.html', context)


@login_required
def createClient(request):
    form = ClientForm()
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, "One new client successfully added!")
            return redirect('audits:client')
        messages.error(request, "There was an Error filling the form, Please re-check!")

    context = {
        'form': form
    }

    
    return render(request, 'audits/client_form.html', context)


class VendorCreate(LoginRequiredMixin, CreateView):
    model = Vendor
    fields = ['name', 'representative', 'designation', 'contact', 'email', 'date_created']
    success_url = reverse_lazy('audits:all-vendor')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(VendorCreate, self).form_valid(form)





@login_required
def vendorDetail(request, pk):
    vendor = Vendor.objects.get(id=pk)
    dates = []
    schedules = Schedule.objects.all()
    sites = []
    for schedule in schedules:
        
        if schedule.vendor == vendor:
            sites.append(schedule.site)
            dates.append(schedule.date_assigned)

    print(dates)
        
    print(sites)
    context = {
        'vendor': vendor,
        'sites': sites,
        'dates': dates
    }
    return render(request, 'audits/vendorDetail.html', context)


@login_required
def updateClient(request, pk):
    client = Client.objects.get(id=pk)
    form = ClientForm(instance=client)
    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('audits:client')

    context = {
        'form': form
    }
    return render(request, 'audits/update_client.html', context)


@login_required
def deleteClient(request, pk):
    client = Client.objects.get(id=pk)
    if request.method == 'POST':
        client.delete()
        return redirect('audits:client')
    context = {
        'client': client
    }
    return render(request, 'audits/delete_client.html', context)


@login_required
def updateSite(request, pk):
    site = Site.objects.get(id=pk)
    form = SiteForm(instance=site)
    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('audits:site')

    context = {
        'form': form
    }
    return render(request, 'audits/update_site.html', context)


@login_required
def deleteSite(request, pk):
    site = Site.objects.get(id=pk)
    if request.method == 'POST':
        site.delete()
        return redirect('audits:site')
    context = {
        'site': site
    }
    return render(request, 'audits/delete_site.html', context)



class VendorUpdate(UpdateView):
    model = Vendor
    template_name = 'audits/update_vendor.html'
    success_url = reverse_lazy('audits:all-vendor')
    fields = ['name', 'representative', 'designation', 'contact', 'email', 'date_created']


@login_required
def updateVendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    form = VendorForm(instance=vendor)
    if request.method == 'POST':
        form = VendorForm(request.POST, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('')

    context = {
        'form': form
    }
    return render(request, 'audits/update_vendor.html', context)


@login_required
def deleteVendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    if request.method == 'POST':
        vendor.delete()
        return redirect('audits:all-vendor')
    context = {
        'vendor': vendor
    }
    return render(request, 'audits/delete_vendor.html', context)


@login_required
def createSchedule(request):

    form = ScheduleForm()
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'audits/site_schedule.html', context)


class ChecklistWizardView(SessionWizardView):
    template_name = "audits/temp.html"
    form_list = [
        PageOneForm, PageTwoForm, PageThreeForm, PageFourForm, PageFiveForm, PageSixForm, PageSevenForm
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    

    def done(self, form_list, form_dict, **kwargs):
        page_1 = form_dict['0'].save()
        page_2 = form_dict['1'].save()
        page_3 = form_dict['2'].save()
        page_4 = form_dict['3'].save()
        page_5 = form_dict['4'].save()
        page_6 = form_dict['5'].save()
        page_7 = form_dict['6'].save()
        
       # Creating Checklist object
        ChecklistForBank.objects.create(
            page_one=page_1,
            page_two=page_2,
            page_three=page_3,
            page_four=page_4,
            page_five=page_5,
            page_six=page_6,
            page_seven=page_7,  
            )
        messages.success(self.request, 'You have successfully submitted the report')
        return redirect('audits:all-vendor')
        


    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())

        except KeyError:
            return super().get(request, *args, **kwargs)




class ChecklistTwoWizardView(SessionWizardView):
    template_name = "audits/temp_2.html"
    form_list = [
        FillingStationPageOneForm, FillingStationPageTwoForm
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    

    def done(self, form_list, form_dict, **kwargs):
        page_1 = form_dict['0'].save()
        page_2 = form_dict['1'].save()
        
       # Creating Checklist object
        ChecklistForFillingStation.objects.create(
            page_one=page_1,
            page_two=page_2,  
            )
        messages.success(self.request, 'You have successfully submitted the report')
        return redirect('audits:all-vendor')
        
    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())

        except KeyError:
            return super().get(request, *args, **kwargs)



class ChecklistThreeWizardView(SessionWizardView):
    template_name = "audits/temp_3.html"
    form_list = [
        CommercialIndustryPageOneForm, CommercialIndustryPageTwoForm
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    

    def done(self, form_list, form_dict, **kwargs):
        page_1 = form_dict['0'].save()
        page_2 = form_dict['1'].save()
        
       # Creating Checklist object
        ChecklistForCandI.objects.create(
            page_one=page_1,
            page_two=page_2,  
            )
        messages.success(self.request, 'You have successfully submitted the report')
        return redirect('audits:all-vendor')
        
    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())

        except KeyError:
            return super().get(request, *args, **kwargs)












































































































# Create your views here.

# Schedule.objects.filter(vendors__name='Supremo')
# Vendor.objects.filter(schedule__status='Sheduled for Audit')
# Site.objects.filter(schedule__status='Sheduled for Audit')
# Site.objects.filter(schedule__report_received=False)
# supremo.schedule_set.all()