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
       


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = '__all__'
        widgets = {'date_created': DateInput()}
       


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'
        widgets = {'date_assigned': DateInput()}




class PageOneForm(forms.ModelForm):

    class Meta:
        model = Checklist
        fields = (
             'client', 'branch', 'site_address', 'site_code', 'latitude', 'longitude', 'business_type', 'contact_person_name', 'contact_personPhone', 
             'vendor', 'auditor_name', 'auditor_phone', 'auditDate', 'location', 'split_1',
             'split_2', 'split_3', 'split_4', 'standing_unit_1', 'standing_unit_2', 'standing_unit_3', 'comment', 
             'florescent', 'led', 'halogen', 'energy_saver', 'panel_light', 'other_lights',
         )
        widgets = {'auditDate': DateInput()}



class PageTwoForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = (
            'desktop', 'laptop', 'printer', 'counting_machine', 'scanner', 'atms', 'tv', 'water_dispenser',
            'exchange_rate_board', 'signage_light', 'water_pump', 'fan', 'microwave', 'card_printer', 'time_stamping_machine',
            'shredder', 'sorting_machine', 'fridge', 'mantrap_door', 'hand_dryer', 'other_appliances',
        )
        


class PageThreeForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = (
            'connects_to_grid', 'connects_to_generator', 'connects_to_solar', 'details', 'grid_avg_cost', 'diesel_avg_cost', 'gensets_maintenance_avg_cost', 
            'ac_maintenance_avg_cost', 'other_cost','genset_1', 'genset_2', 'genset_3', 'genset_4', 'transformer_1', 'transformer_2', 'noOfAtm', 'otherAtmDetails', 
            'opening_time', 'closing_time', 'Monday_to_Friday', 'Monday_to_Saturday', 'Monday_to_Sunday', 'item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7',
            'inverter_1', 'inverter_2', 'inverter_3', 'ups_1', 'ups_2', 'ups_3', 'stabilizer_1', 'stabilizer_2',
            'battery_bank_1', 'battery_bank_2', 'battery_bank_3', 'battery_bank_4', 
        )



class PageFourForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = (
            'bungalow', 'one_storey', 'two_storey', 'three_storey', 'multi_resident', 'multi_commercial', 'mall', 'ownership',
            'picture', 'roof_type', 'roof_picture', 'roof_length', 'roof_width', 'total_area', 'number_of_panels', 'roofing_sheet_material', 
            'roofing_truss_material', 'roofing_sheet_thickness','roofing_truss_spacing', 'repair_needed', 'minor_repair', 'major_repair', 'complete_replacement', 'changeover_box_picture', 
            'Distribution_board_picture', 'general_comment', 
        )


class PageFiveForm(forms.ModelForm):
    class Meta:
        model = Checklist
        fields = (
            'er_available', 'space_toBuild', 'on_what_floor', 'dimension', 'ER_picture_or_space_to_build', 
            'distance_to_generator', 'distance_to_powerRoom', 'distance_to_roof', 'one', 'two', 'three', 'four', 'five', 'six',
            'seven', 'eight', 'nine', 'ten',
            'client_rep', 'position', 'client_repPhone', 'email', 'GeneralComment'
        )





class FillingStationPageOneForm(forms.ModelForm):
    class Meta:
        model = Checklist2
        fields = (
            'client', 'branch', 'site_address', 'site_code', 'latitude', 'longitude', 'business_type', 
            'contact_person_name', 'contact_personPhone', 'vendor', 'auditor_name', 'auditor_phone', 'auditDate', 
            'pms_pump', 'ago_pump', 'dpk_pump', 'surface_transfer_pump', 'water_pump', 'location', 'split_1',
            'split_2', 'split_3', 'split_4', 'standing_unit_1', 'standing_unit_2', 'standing_unit_3',
            
        )
        widgets = {'auditDate': DateInput()}


class FillingStationPageTwoForm(forms.ModelForm):
    class Meta:
        model = Checklist2
        fields = (
            'florescent', 'led', 'halogen', 'energy_saver', 'panel_light', 'other_lights',
            'generator_1', 'generator_2', 'connects_to_grid', 'fridge', 'freezer', 'fan',
            'printer', 'scanner', 'note_counting_machine', 'others_equipment', 'three_phase_equipment',
            'size'
        )

class FillingStationPageThreeForm(forms.ModelForm):
    class Meta:
        model = Checklist2
        fields = (
            'roof_type', 'roof_material', 'roofing_sheet_thickness', 'roofing_truss_material', 'ER_picture_or_space_to_build',
            'building_picture', 'roof_picture', 'changeover_box_picture', 'Distribution_board_picture', 'opening_time', 'closing_time',
            'one', 'two', 'three', 'four', 'five', 'six',
            'seven', 'eight', 'nine', 'ten',
            'client_rep', 'position', 'client_repPhone', 'email', 'GeneralComment'
        )
        


class CommercialIndustryPageOneForm(forms.ModelForm):
    class Meta:
        model = Checklist3
        fields = (
            'client', 'branch', 'site_address', 'site_code', 'latitude', 'longitude', 'business_type', 
            'contact_person_name', 'contact_personPhone', 'vendor', 'auditor_name', 'auditor_phone', 'auditDate', 
            'connects_to_grid', 'reasons', 'grid_quality', 'grid_availability', 'day', 'night', 'transformer_1', 
            'transformer_2', 'transformer_3', 'transformer_4', 'transformer_5','transformer_6', 'transformer_7',
            'transformer_8', 'transformer_9', 'transformer_10','tariff', 'genset_1', 'genset_2', 'genset_3', 'genset_4',
            'genset_5', 'genset_6'
        )
        widgets = {'auditDate': DateInput()}


class CommercialIndustryPageTwoForm(forms.ModelForm):
    class Meta:
        model = Checklist3
        fields = (
            'switching_mode', 'availability_of_synchPanel', 'synchPanelSize', 'spareBreaker', 'breakerSize', 'minimum_load', 'average_dayLoad', 'average_nightLoad',
            'maximum_load', 'daily_consumption', 'backupSize', 'building_type', 'roof_space_1', 'roof_space_2', 
            'roof_space_3', 'roof_space_4', 'roofing_truss_material', 'roofing_sheet_thickness', 'roof_picture', 'ground_space_1', 'ground_space_2', 
            'ground_space_picture', 'equipment_room_availability', 'size_of_equipment_room', 'ER_picture_or_space_to_build','panel_room_picture', 
            'roof_to_ER_distance', 'ER_to_power_room_distance', 'opening_time','closing_time', 'client_rep', 'position', 'client_repPhone', 'email', 'GeneralComment'
        )
       

