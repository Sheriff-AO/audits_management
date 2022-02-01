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
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['allSites'] = Site.objects.all().count()
        return context



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

def summary(request):
    sites = Site.objects.all().count()
    smesClients = Client.objects.filter(category="SMEs").count()
    candIClients = Client.objects.filter(category="C&I").count()
    totalClients = Client.objects.all().count()
    schedules = Schedule.objects.all().count()
    audited = Schedule.objects.filter(status='Audited').count()
    pendingAudit = Schedule.objects.filter(status='Pending Audit').count()
    vendors = Vendor.objects.all().count()
    
    # site = Site.objects.filter(status='Pending').count()
    
    context = {
        'sites': sites,
        'smesClients': smesClients,
        'candIClients': candIClients,
        'totalClients': totalClients,
        'schedules': schedules,
        'vendors': vendors,
        'audited': audited,
        'pendingAudit': pendingAudit,
    }
    return render(request, 'audits/summary.html', context)


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
        PageOneForm, PageTwoForm, PageThreeForm, PageFourForm, PageFiveForm
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    

    def done(self, form_list, form_dict, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        #print("FORM DATA",form_data)
        checklist = Checklist(
            client=form_data[0]['client'], branch=form_data[0]['branch'], site_address=form_data[0]['site_address'], site_code=form_data[0]['site_code'], latitude=form_data[0]['latitude'],
            longitude=form_data[0]['longitude'], business_type=form_data[0]['business_type'], contact_person_name=form_data[0]['contact_person_name'], vendor=form_data[0]['vendor'],
            auditor_name=form_data[0]['auditor_name'],
            auditor_phone=form_data[0]['auditor_phone'], auditDate=form_data[0]['auditDate'], location=form_data[0]['location'], split_1=form_data[0]['split_1'], split_2=form_data[0]['split_2'],
            split_3=form_data[0]['split_3'], split_4=form_data[0]['split_4'], standing_unit_1=form_data[0]['standing_unit_1'], standing_unit_2=form_data[0]['standing_unit_2'], standing_unit_3=form_data[0]['standing_unit_3'],
            comment=form_data[0]['comment'], florescent=form_data[0]['florescent'], led=form_data[0]['led'], halogen=form_data[0]['halogen'], energy_saver=form_data[0]['energy_saver'],
            panel_light=form_data[0]['panel_light'], other_lights=form_data[0]['other_lights'], desktop=form_data[1]['desktop'], laptop=form_data[1]['laptop'], printer=form_data[1]['printer'],
            counting_machine=form_data[1]['counting_machine'], scanner=form_data[1]['scanner'], atms=form_data[1]['atms'], tv=form_data[1]['tv'], water_dispenser=form_data[1]['water_dispenser'],
            exchange_rate_board=form_data[1]['exchange_rate_board'], signage_light=form_data[1]['signage_light'], water_pump=form_data[1]['water_pump'], fan=form_data[1]['fan'], microwave=form_data[1]['microwave'],
            card_printer=form_data[1]['card_printer'], time_stamping_machine=form_data[1]['time_stamping_machine'], shredder=form_data[1]['shredder'], sorting_machine=form_data[1]['sorting_machine'], fridge=form_data[1]['fridge'],
            mantrap_door=form_data[1]['mantrap_door'], hand_dryer=form_data[1]['hand_dryer'], other_appliances=form_data[1]['other_appliances'], connects_to_grid=form_data[2]['connects_to_grid'],
            connects_to_generator=form_data[2]['connects_to_generator'],
            connects_to_solar=form_data[2]['connects_to_solar'], details=form_data[2]['details'], grid_avg_cost=form_data[2]['grid_avg_cost'], diesel_avg_cost=form_data[2]['diesel_avg_cost'], 
            gensets_maintenance_avg_cost=form_data[2]['gensets_maintenance_avg_cost'],
            ac_maintenance_avg_cost=form_data[2]['ac_maintenance_avg_cost'], other_cost=form_data[2]['other_cost'], genset_1=form_data[2]['genset_1'], genset_2=form_data[2]['genset_2'], genset_3=form_data[2]['genset_3'],
            genset_4=form_data[2]['genset_4'], transformer_1=form_data[2]['transformer_1'], transformer_2=form_data[2]['transformer_2'], noOfAtm=form_data[2]['noOfAtm'], otherAtmDetails=form_data[2]['otherAtmDetails'],
            opening_time=form_data[2]['opening_time'], closing_time=form_data[2]['closing_time'], Monday_to_Friday=form_data[2]['Monday_to_Friday'], Monday_to_Saturday=form_data[2]['Monday_to_Saturday'], Monday_to_Sunday=form_data[2]['Monday_to_Sunday'],
            item1=form_data[2]['item1'], item2=form_data[2]['item2'], item3=form_data[2]['item3'], item4=form_data[2]['item4'], item5=form_data[2]['item5'],
            item6=form_data[2]['item6'], item7=form_data[2]['item7'], inverter_1=form_data[2]['inverter_1'], inverter_2=form_data[2]['inverter_2'], inverter_3=form_data[2]['inverter_3'],
            ups_1=form_data[2]['ups_1'], ups_2=form_data[2]['ups_2'], ups_3=form_data[2]['ups_3'], stabilizer_1=form_data[2]['stabilizer_1'], stabilizer_2=form_data[2]['stabilizer_2'],
            battery_bank_1=form_data[2]['battery_bank_1'], battery_bank_2=form_data[2]['battery_bank_2'], battery_bank_3=form_data[2]['battery_bank_3'], battery_bank_4=form_data[2]['battery_bank_4'], 
            bungalow=form_data[3]['bungalow'], one_storey=form_data[3]['one_storey'], two_storey=form_data[3]['two_storey'], three_storey=form_data[3]['three_storey'], 
            multi_resident=form_data[3]['multi_resident'], multi_commercial=form_data[3]['multi_commercial'], mall=form_data[3]['mall'], ownership=form_data[3]['ownership'], 
            picture=form_data[3]['picture'], roof_type=form_data[3]['roof_type'], roof_picture=form_data[3]['roof_picture'], roof_length=form_data[3]['roof_length'], 
            roof_width=form_data[3]['roof_width'], total_area=form_data[3]['total_area'], number_of_panels=form_data[3]['number_of_panels'], roofing_sheet_material=form_data[3]['roofing_sheet_material'], 
            roofing_truss_material=form_data[3]['roofing_truss_material'], roofing_truss_spacing=form_data[3]['roofing_truss_spacing'], repair_needed=form_data[3]['repair_needed'], minor_repair=form_data[3]['minor_repair'], 
            major_repair=form_data[3]['major_repair'], complete_replacement=form_data[3]['complete_replacement'], changeover_box_picture=form_data[3]['changeover_box_picture'], Distribution_board_picture=form_data[3]['Distribution_board_picture'], 
            general_comment=form_data[3]['general_comment'], 
            er_available=form_data[4]['er_available'], space_toBuild=form_data[4]['space_toBuild'], on_what_floor=form_data[4]['on_what_floor'], dimension=form_data[4]['dimension'], 
            ER_picture_or_space_to_build=form_data[4]['ER_picture_or_space_to_build'], distance_to_generator=form_data[4]['distance_to_generator'], distance_to_powerRoom=form_data[4]['distance_to_powerRoom'], one=form_data[4]['one'], 
            two=form_data[4]['two'], three=form_data[4]['three'], four=form_data[4]['four'], five=form_data[4]['five'], 
            six=form_data[4]['six'], seven=form_data[4]['seven'], eight=form_data[4]['eight'], nine=form_data[4]['nine'], ten=form_data[4]['ten'],
            client_rep=form_data[4]['client_rep'], position=form_data[4]['position'], client_repPhone=form_data[4]['client_repPhone'], email=form_data[4]['email'], 
            GeneralComment=form_data[4]['GeneralComment']
        )
        checklist.save()

        return render(self.request, 'audits/done.html', {'data': form_data})
        # page_1 = form_dict['0'].save()
        # page_2 = form_dict['1'].save()
        # page_3 = form_dict['2'].save()
        # page_4 = form_dict['3'].save()
        # page_5 = form_dict['4'].save()
       
        
       # Creating Checklist object
        # ChecklistForBank.objects.create(
        #     page_one=page_1,
        #     page_two=page_2,
        #     page_three=page_3,
        #     page_four=page_4,
        #     page_five=page_5,
             
        #     )
        # messages.success(self.request, 'You have successfully submitted the report')
        # return redirect('audits:all-vendor')
        


    def get(self, request, *args, **kwargs):
        try:
            return self.render(self.get_form())

        except KeyError:
            return super().get(request, *args, **kwargs)




class ChecklistTwoWizardView(SessionWizardView):
    template_name = "audits/temp_2.html"
    form_list = [
        FillingStationPageOneForm, FillingStationPageTwoForm, FillingStationPageThreeForm
    ]

    file_storage = FileSystemStorage(
        location=os.path.join(settings.MEDIA_ROOT, 'photos'))
    

    def done(self, form_list, form_dict, **kwargs):
        form_data = [form.cleaned_data for form in form_list]
        checklist2 = Checklist2(
            client=form_data[0]['client'], branch=form_data[0]['branch'], site_address=form_data[0]['site_address'], site_code=form_data[0]['site_code'], latitude=form_data[0]['latitude'],
            longitude=form_data[0]['longitude'], business_type=form_data[0]['business_type'], contact_person_name=form_data[0]['contact_person_name'], vendor=form_data[0]['vendor'], auditor_name=form_data[0]['auditor_name'],
            auditor_phone=form_data[0]['auditor_phone'], auditDate=form_data[0]['auditDate'], pms_pump=form_data[0]['pms_pump'], ago_pump=form_data[0]['ago_pump'], dpk_pump=form_data[0]['dpk_pump'], 
            surface_transfer_pump=form_data[0]['surface_transfer_pump'], water_pump=form_data[0]['water_pump'],location=form_data[0]['location'], split_1=form_data[0]['split_1'], split_2=form_data[0]['split_2'],
            split_3=form_data[0]['split_3'], split_4=form_data[0]['split_4'], standing_unit_1=form_data[0]['standing_unit_1'], standing_unit_2=form_data[0]['standing_unit_2'], 
            standing_unit_3=form_data[0]['standing_unit_3'], florescent=form_data[1]['florescent'],
            led=form_data[1]['led'], halogen=form_data[1]['halogen'], energy_saver=form_data[1]['energy_saver'], panel_light=form_data[1]['panel_light'],
            other_lights=form_data[1]['other_lights'], generator_1=form_data[1]['generator_1'], generator_2=form_data[1]['generator_2'], connects_to_grid=form_data[1]['connects_to_grid'],
            fridge=form_data[1]['fridge'], freezer=form_data[1]['freezer'], fan=form_data[1]['fan'], printer=form_data[1]['printer'],
            note_counting_machine=form_data[1]['note_counting_machine'], others_equipment=form_data[1]['others_equipment'], three_phase_equipment=form_data[1]['three_phase_equipment'], size=form_data[1]['size'],
            roof_type=form_data[2]['roof_type'], roof_material=form_data[2]['roof_material'], roofing_sheet_thickness=form_data[2]['roofing_sheet_thickness'], roofing_sheet_lapping=form_data[2]['roofing_sheet_lapping'],
            roofing_truss_material=form_data[2]['roofing_truss_material'], ER_picture_or_space_to_build=form_data[2]['ER_picture_or_space_to_build'], building_picture=form_data[2]['building_picture'], roof_picture=form_data[2]['roof_picture'],
            changeover_box_picture=form_data[2]['changeover_box_picture'], Distribution_board_picture=form_data[2]['Distribution_board_picture'], opening_time=form_data[2]['opening_time'], closing_time=form_data[2]['closing_time'],
            one=form_data[2]['one'], 
            two=form_data[2]['two'], three=form_data[2]['three'], four=form_data[2]['four'], five=form_data[2]['five'], 
            six=form_data[2]['six'], seven=form_data[2]['seven'], eight=form_data[2]['eight'], nine=form_data[2]['nine'], ten=form_data[2]['ten'],
            client_rep=form_data[2]['client_rep'], position=form_data[2]['position'], client_repPhone=form_data[2]['client_repPhone'], email=form_data[2]['email'], 
            GeneralComment=form_data[2]['GeneralComment']
        )
        checklist2.save()
        messages.success(self.request, 'You have successfully submitted the report')
        return redirect('audits:all-vendor')
        #return render(self.request, 'audits/done1.html', {'data': form_data})
        # page_1 = form_dict['0'].save()
        # page_2 = form_dict['1'].save()
        
       # Creating Checklist object
        # Checklist2.objects.create(
        #     page_one=page_1,
        #     page_two=page_2,  
        #     )
        # 
        # 
        
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
        form_data = [form.cleaned_data for form in form_list]
        checklist3 = Checklist3(
            client=form_data[0]['client'], branch=form_data[0]['branch'], site_address=form_data[0]['site_address'], site_code=form_data[0]['site_code'],
            latitude=form_data[0]['latitude'], longitude=form_data[0]['longitude'], business_type=form_data[0]['business_type'], contact_person_name=form_data[0]['contact_person_name'], vendor=form_data[0]['vendor'],
            auditor_name=form_data[0]['auditor_name'], auditor_phone=form_data[0]['auditor_phone'], auditDate=form_data[0]['auditDate'], connects_to_grid=form_data[0]['connects_to_grid'],
            reasons=form_data[0]['reasons'], grid_quality=form_data[0]['grid_quality'], grid_availability=form_data[0]['grid_availability'], day=form_data[0]['day'],
            night=form_data[0]['night'], transformer_1=form_data[0]['transformer_1'], transformer_2=form_data[0]['transformer_2'], transformer_3=form_data[0]['transformer_3'],
            transformer_4=form_data[0]['transformer_4'], transformer_5=form_data[0]['transformer_5'], transformer_6=form_data[0]['transformer_6'], transformer_7=form_data[0]['transformer_7'],
            transformer_8=form_data[0]['transformer_8'], transformer_9=form_data[0]['transformer_9'], transformer_10=form_data[0]['transformer_10'], tariff=form_data[0]['tariff'],
            genset_1=form_data[0]['genset_1'], genset_2=form_data[0]['genset_2'], genset_3=form_data[0]['genset_3'], genset_4=form_data[0]['genset_4'],
            genset_5=form_data[0]['genset_5'], genset_6=form_data[0]['genset_6'],
            switching_mode=form_data[1]['switching_mode'], availability_of_synchPanel=form_data[1]['availability_of_synchPanel'], synchPanelSize=form_data[1]['synchPanelSize'], minimum_load=form_data[1]['minimum_load'],
            average_dayLoad=form_data[1]['average_dayLoad'], average_nightLoad=form_data[1]['average_nightLoad'], maximum_load=form_data[1]['maximum_load'], daily_consumption=form_data[1]['daily_consumption'],
            backupSize=form_data[1]['backupSize'], building_type=form_data[1]['building_type'], roof_space_1=form_data[1]['roof_space_1'], roof_space_2=form_data[1]['roof_space_2'],
            roof_space_3=form_data[1]['roof_space_3'], roof_space_4=form_data[1]['roof_space_4'], roofing_truss_material=form_data[1]['roofing_truss_material'], roofing_sheet_thickness=form_data[1]['roofing_sheet_thickness'],
            roof_picture=form_data[1]['roof_picture'], ground_space_1=form_data[1]['ground_space_1'], ground_space_2=form_data[1]['ground_space_2'], ground_space_picture=form_data[1]['ground_space_picture'],
            equipment_room_availability=form_data[1]['equipment_room_availability'], size_of_equipment_room=form_data[1]['size_of_equipment_room'], ER_picture_or_space_to_build=form_data[1]['ER_picture_or_space_to_build'], panel_room_picture=form_data[1]['panel_room_picture'],
            roof_to_ER_distance=form_data[1]['roof_to_ER_distance'], ER_to_power_room_distance=form_data[1]['ER_to_power_room_distance'],
            opening_time=form_data[1]['opening_time'], closing_time=form_data[1]['closing_time'],
            client_rep=form_data[1]['client_rep'], position=form_data[1]['position'], client_repPhone=form_data[1]['client_repPhone'], email=form_data[1]['email'], 
            GeneralComment=form_data[1]['GeneralComment']
        )
        checklist3.save()

        return render(self.request, 'audits/done3.html', {'data': form_data})

    #     page_1 = form_dict['0'].save()
    #     page_2 = form_dict['1'].save()
        
    #    # Creating Checklist object
    #     Checklist3.objects.create(
    #         page_one=page_1,
    #         page_two=page_2,  
    #         )
        # messages.success(self.request, 'You have successfully submitted the report')
        # return redirect('audits:all-vendor')
        
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