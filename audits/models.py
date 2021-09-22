from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.translation import gettext as _
from django.db.models.fields.reverse_related import ManyToOneRel

# Create your models here.

class Client(models.Model):
    CATEGORY = (
        ('SMEs', 'Banking & SMEs'),
        ('C&I', 'Commercial & Industries'),
    )
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    name = models.CharField(max_length=200, null=True)
    rep_name = models.CharField(max_length=200, null=True)
    designation = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=26, null=True)
    email = models.EmailField(max_length=100, null=True)
    num_of_site = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('date_created',)

    
class Site(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    address = models.TextField(max_length=200, null=True)
    state = models.CharField(max_length=20, null=True)
    region = models.CharField(max_length=4, null=True)
    contact = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=100, null=True)
    phone = models.CharField(max_length=26, null=True)
    date_added = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('date_added',)



class Vendor(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    representative = models.CharField(max_length=100, null=True)
    designation = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=26, null=True)
    email = models.EmailField(max_length=100, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    sites = models.ManyToManyField(Site, blank=True, through='Schedule')
    

    def __str__(self):
        return str(self.name) if (self.name) else ""

    class Meta:
        ordering = ('-date_created',)


# Schedule.objects.filter(vendors__name='Supremo')
# Vendor.objects.filter(schedule__status='Sheduled for Audit')
# Site.objects.filter(schedule__status='Sheduled for Audit')
# Site.objects.filter(schedule__report_received=False)
# supremo.schedule_set.all()

class Schedule(models.Model):
    STATUS = (
        ('Scheduled for Audit', 'Scheduled for Audit'),
        ('Scheduled for Data-logging', 'Scheduled for Data-logging'),
        ('Scheduled for Audit & Data-logging', 'Scheduled for Audit & Data-logging'),
        ('Pending Schedule', 'Pending Schedule'),
        ('Audited', 'Audited'),
        ('Data-logged', 'Data-logged'),
        ('Audited & Data-logged', 'Audited & Data-logged'),
    )
    vendor = models.ForeignKey(Vendor, null=True, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, null=True, on_delete=models.CASCADE)
    date_assigned = models.DateTimeField()
    status = models.CharField(max_length=100, null=True, choices=STATUS)
    report_received = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vendor} - {self.site}"

    class Meta:
        ordering = ('date_assigned',)



class PageOne(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    site_full_address = models.CharField(max_length=120, null=True, blank=True)
    gps_coordinate = models.CharField(max_length=30, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField()
    location = models.TextField(_("ACs by Location"), null=True, help_text='Please enter the number of ACs per location.')
    split_1 = models.IntegerField(_("Number of 1HP"), null=True)
    split_2 = models.IntegerField(_("Number of 1.5HP"), null=True)
    split_3 = models.IntegerField(_("Number of 2HP"), null=True)
    split_4 = models.IntegerField(_("Number of 2.5HP"), null=True)
    standing_unit_1 = models.IntegerField(_("Number of 3HP"), null=True)
    standing_unit_2 = models.IntegerField(_("Number of 5HP"), null=True)
    standing_unit_3 = models.IntegerField(_("Number of 10HP"), null=True)
    comment = models.TextField(_("Comment"), null=True)
    rooftop = models.BooleanField(default=False, null=True)
    ground_mounted = models.BooleanField(default=False, null=True)
    rooftop_ground_mounted = models.BooleanField(default=False, null=True)
    florescent = models.CharField(max_length=50, null=True, blank=True)
    LED = models.CharField(max_length=50, null=True, blank=True)
    halogen = models.CharField(max_length=50, null=True, blank=True)
    energy_saver = models.CharField(max_length=50, null=True, blank=True)
    panel_light = models.CharField(max_length=50, null=True, blank=True)
    others = models.CharField(max_length=50, null=True, blank=True, help_text='Please state the power rating in Watts.')


    class Meta:
        verbose_name = 'PageOne'
        verbose_name_plural = 'PageOnes'





class PageTwo(models.Model):
    desktop = models.IntegerField(null=True, blank=True)
    laptop = models.IntegerField(null=True, blank=True)
    printer = models.IntegerField(null=True, blank=True)
    counting_machine = models.IntegerField(null=True, blank=True)
    scanner = models.IntegerField(null=True, blank=True)
    atms = models.IntegerField(null=True, blank=True)
    tv = models.IntegerField(null=True, blank=True)
    water_dispenser = models.IntegerField(null=True, blank=True)
    exchange_rate_board = models.IntegerField(null=True, blank=True)
    signage_light = models.IntegerField(null=True, blank=True)
    water_pump = models.IntegerField(null=True, blank=True)
    fan = models.IntegerField(null=True, blank=True)
    microwave = models.IntegerField(null=True, blank=True)
    card_printer = models.IntegerField(null=True, blank=True)
    time_stamping_machine = models.IntegerField(null=True, blank=True)
    shredder = models.IntegerField(null=True, blank=True)
    sorting_machine = models.IntegerField(null=True, blank=True)
    fridge = models.IntegerField(null=True, blank=True)
    mantrap_door = models.IntegerField(null=True, blank=True)
    hand_dryer = models.IntegerField(null=True, blank=True)
    others = models.TextField(null=True, blank=True, help_text='Please enter the name and counts of other appliances if exist.')


class PageThree(models.Model):
    connects_to_grid = models.BooleanField(null=True)
    connects_to_solar = models.BooleanField(null=True)
    details = models.CharField(max_length=200, help_text='Enter the number and size of the solar panels.')
    connects_to_generator = models.BooleanField(null=True)
    size_of_transformer = models.IntegerField(null=True, help_text='in kVA')
    genset_1 = models.CharField(max_length=60, null=True, blank=True)
    genset_2 = models.CharField(max_length=60, null=True, blank=True)
    genset_3 = models.CharField(max_length=60, null=True, blank=True)
    transformer = models.CharField(max_length=60, null=True, blank=True)
    item1 = models.CharField(max_length=100, null=True, blank=True, help_text='State the equipment/appliance name and the rating in kW or kVA in each case. ')
    item2 = models.CharField(max_length=100, null=True, blank=True)
    item3 = models.CharField(max_length=100, null=True, blank=True)
    item4 = models.CharField(max_length=100, null=True, blank=True)
    item5 = models.CharField(max_length=100, null=True, blank=True)
    item6 = models.CharField(max_length=100, null=True, blank=True)
    item7 = models.CharField(max_length=100, null=True, blank=True)
    inverter_1 = models.CharField(max_length=100, null=True, blank=True)
    inverter_2 = models.CharField(max_length=100, null=True, blank=True)
    inverter_3 = models.CharField(max_length=100, null=True, blank=True)
    ups_1 = models.CharField(max_length=100, null=True, blank=True)
    ups_2 = models.CharField(max_length=100, null=True, blank=True)
    ups_3 = models.CharField(max_length=100, null=True, blank=True)
    stabilizer_1 = models.CharField(max_length=100, null=True, blank=True)
    stabilizer_2 = models.CharField(max_length=100, null=True, blank=True)
    battery_bank_1 = models.CharField(max_length=100, null=True, blank=True, help_text='e.g 24 units of 12V 200AH')
    battery_bank_2 = models.CharField(max_length=100, null=True, blank=True)
    battery_bank_3 = models.CharField(max_length=100, null=True, blank=True)
    battery_bank_4 = models.CharField(max_length=100, null=True, blank=True)






class PageFour(models.Model):
    opening_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    closing_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    monday_to_friday = models.BooleanField(default=False)
    monday_to_saturday = models.BooleanField(default=False)
    monday_to_sunday = models.BooleanField(default=False)
    available = models.BooleanField(default=False, help_text='Only tick if equipment room is available.')
    not_available = models.BooleanField(default=False, help_text='Only tick if equipment room is NOT available.')
    on_what_floor = models.CharField(max_length=20, null=True, blank=True)
    dimension = models.CharField(max_length=30, null=True, blank=True)
    distance_to_generator = models.CharField(max_length=10, null=True, blank=True)
    
    ER_picture_or_space_to_build = models.ImageField(default='default5.jpg',  upload_to='er_pics')
    bungalow = models.BooleanField(default=False, help_text='State the building type and other information as below.')
    one_storey = models.BooleanField(default=False)
    two_storey = models.BooleanField(default=False)
    three_storey = models.BooleanField(default=False)
    multi_resident = models.BooleanField(default=False)
    multi_commercial = models.BooleanField(default=False)
    mall = models.BooleanField(default=False)
    building_picture = models.ImageField(
        default='default1.jpg',  upload_to='building_pics')
    roof_picture = models.ImageField(
        default='default2.jpg', upload_to='roof_pics')
    changeover_box_picture = models.ImageField(
        default='default3.jpg',  upload_to='changeover_pics')
    Distribution_board_picture = models.ImageField(
        default='default4.jpg', upload_to='db_pics')
   


class PageFive(models.Model):
    one = models.BooleanField( _("Will ladder or scaffolds be required for access to the roof?"), default=False, null=True)
    two = models.BooleanField( _("Will fall protection be required while working on the roof?"), default=False, null=True)
    three = models.BooleanField( _("Is there enough access and egress at proposed equipment room?"), default=False, null=True)
    four = models.BooleanField( _("Does the proposed equipment room has an existing smoke/fire alarm?"), default=False, null=True)
    five = models.BooleanField( _("Is there enough access and egress at the generator area. If we are dealing with a confined space please state?"), default=False, null=True)
    six = models.BooleanField( _("Are there existing bund walls/secondary spill contigency arrangement around the diesel storage tank?"), default=False, null=True)
    seven = models.BooleanField( _("Are there visible signs of oil spillage around the generator area/plinth? Please take date-staped pictures"), default=False, null=True)
    eight = models.BooleanField(
        _("Are there any overhead power cables that will be a problem for work at height?"), default=False, null=True)
    nine = models.BooleanField( _("Are there any environmental or safety concerns?"), default=False, null=True)   

    

class PageSix(models.Model):
    roof_dimension = models.CharField(max_length=20, null=True, blank=True)
    total_area = models.IntegerField()
    number_of_panels = models.IntegerField()
    roof_type = models.CharField(max_length=50, null=True, blank=True)
    roofing_sheet_material = models.CharField(max_length=20, null=True, blank=True)
    roofing_sheet_thickness = models.CharField(max_length=20, null=True, blank=True)
    roofing_sheet_lapping = models.CharField(max_length=20, null=True, blank=True)
    roofing_truss = models.CharField(max_length=20, null=True, blank=True)
    not_needed = models.BooleanField(default=False, help_text='Roof Remedial work?')
    minor_repair = models.BooleanField(default=False)
    major_repair = models.BooleanField(default=False)
    complete_replacement = models.BooleanField(default=False)
    general_comment = models.TextField(null=True, blank=True)


class PageSeven(models.Model):    
    name = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)




class ChecklistForBank(models.Model):
    page_one = models.OneToOneField("audits.PageOne", verbose_name=_("Customer Information | Cooling | Roof and Lightings"), on_delete=models.CASCADE)
    page_two = models.OneToOneField("audits.PageTwo", verbose_name=_("Appliances"), on_delete=models.CASCADE)
    page_three = models.OneToOneField("audits.PageThree", verbose_name=_("Existing Power Information"), on_delete=models.CASCADE)
    page_four = models.OneToOneField("audits.PageFour", verbose_name=_("Operation Hours | Building | ER Information"), on_delete=models.CASCADE)
    page_five = models.OneToOneField("audits.PageFive", verbose_name=_("Safety"), on_delete=models.CASCADE)
    page_six = models.OneToOneField("audits.PageSix", verbose_name=_("Roof Information"), on_delete=models.CASCADE)
    page_seven = models.OneToOneField("audits.PageSeven", verbose_name=_("Signoff | General Comments"), on_delete=models.CASCADE)


class FillingStationPageOne(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    site_full_address = models.CharField(max_length=120, null=True, blank=True)
    gps_coordinate = models.CharField(_("GPS Coordinates"), max_length=30, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField()
    PMS_pump = models.IntegerField(null=True, blank=True)   
    AGO_pump = models.IntegerField(null=True, blank=True)   
    DPK_pump = models.IntegerField(null=True, blank=True)  
    surface_transfer_pump = models.IntegerField(null=True, blank=True, help_text='1.5HP')   
    water_pump = models.IntegerField(null=True, blank=True)   
    location = models.TextField(_("ACs by Location"), null=True, help_text='Please enter the number of ACs by location, stating the codition as: working or not working.')
    split_1 = models.IntegerField(_("Number of 1HP"), null=True) 
    split_2 = models.IntegerField(_("Number of 1.5HP"), null=True)
    split_3 = models.IntegerField(_("Number of 2HP"), null=True)
    split_4 = models.IntegerField(_("Number of 2.5HP"), null=True)
    standing_unit_1 = models.IntegerField(_("Number of 3HP"), null=True)
    standing_unit_2 = models.IntegerField(_("Number of 5HP"), null=True)
    standing_unit_3 = models.IntegerField(_("Number of 10HP"), null=True)
    lighting_details = models.CharField(max_length=200, null=True, blank=True, help_text='Please state the type and wattage rating of all bulbs.')
    canopy_light = models.IntegerField(null=True, blank=True)
    perimeter_light = models.IntegerField(null=True, blank=True)
    offices = models.IntegerField(null=True, blank=True)
    rest_rooms = models.IntegerField(null=True, blank=True)
    others_1 = models.IntegerField(null=True, blank=True)
    others_2 = models.IntegerField(null=True, blank=True)
    generator_1 = models.IntegerField(null=True, blank=True)
    generator_2 = models.IntegerField(null=True, blank=True)
    connects_to_grid = models.BooleanField(null=True)
    transformer_size = models.IntegerField(null=True, blank=True, help_text='in kVA')
    fridge = models.IntegerField(null=True, blank=True)
    freezer = models.IntegerField(null=True, blank=True)
    fan = models.IntegerField(null=True, blank=True)
    printer = models.IntegerField(null=True, blank=True)
    scanner = models.IntegerField(null=True, blank=True)



class FillingStationPageTwo(models.Model):
    note_counting_machine = models.IntegerField(null=True, blank=True)
    others_equipment_1 = models.IntegerField(null=True, blank=True)
    others_equipment_2 = models.IntegerField(null=True, blank=True)
    others_equipment_3 = models.IntegerField(null=True, blank=True)
    others_equipment_4 = models.IntegerField(null=True, blank=True)
    three_phase_equipment = models.BooleanField(help_text='State the size of te three pahse equipment (in HP) below')
    size = models.IntegerField(null=True, blank=True)
    roof_type = models.CharField(max_length=200, null=True, blank=True, help_text='Flat, Mono-Pitch, Double-Pitch, Specify if others')
    roof_material = models.CharField(max_length=30, null=True, blank=True, help_text='Concrete slab, Aluminum, Ardex, Specify if others')
    roofing_sheet_thickness = models.IntegerField(null=True, help_text='if Aluminum')
    roofing_sheet_lapping = models.CharField(max_length=40, null=True, blank=True)
    roofing_truss_material = models.CharField(max_length=40, null=True, blank=True)  
    ER_picture_or_space_to_build = models.ImageField(default='default5.jpg',  upload_to='er_pics')
    bungalow = models.BooleanField(default=False, help_text='State the building type and other information as below.')
    one_storey = models.BooleanField(default=False)
    two_storey = models.BooleanField(default=False)
    three_storey = models.BooleanField(default=False)
    multi_resident = models.BooleanField(default=False)
    multi_commercial = models.BooleanField(default=False)
    mall = models.BooleanField(default=False)
    building_picture = models.ImageField(
        default='default1.jpg',  upload_to='building_pics')
    roof_picture = models.ImageField(
        default='default2.jpg', upload_to='roof_pics')
    changeover_box_picture = models.ImageField(
        default='default3.jpg',  upload_to='changeover_pics')
    Distribution_board_picture = models.ImageField(
        default='default4.jpg', upload_to='db_pics')
    opening_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    closing_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    starsight_rep = models.CharField(_('Starsight Representative'),max_length=50, null=True, blank=True)
    starsight_contact_number = models.CharField(max_length=30, null=True, blank=True)
    station_rep = models.CharField(_("Station Representative"),max_length=30, null=True, blank=True)
    client_contact_number = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(_("General Comments"), null=True, blank=True) 



    
class ChecklistForFillingStation(models.Model):
    page_one = models.OneToOneField("audits.FillingStationPageOne", 
    verbose_name=_("Pumps | Cooling and Lighting Information"), on_delete=models.CASCADE)
    page_two = models.OneToOneField("audits.FillingStationPageTwo", 
    verbose_name=_("Appliances | Roof Detail and Operation Hour Information"), on_delete=models.CASCADE)
   


   
class CommercialIndustryPageOne(models.Model):
    client = models.ForeignKey(Client, null=True, on_delete=models.CASCADE)
    site_full_address = models.CharField(max_length=120, null=True, blank=True)
    gps_coordinate = models.CharField(_("GPS Coordinates"), max_length=30, null=True, blank=True)
    contact_person = models.CharField(max_length=100, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    date = models.DateTimeField()
    connects_to_grid = models.BooleanField(null=True, blank=True)
    tariff = models.DecimalField(null=True, blank=True, max_digits=8, decimal_places=4, help_text='per kWh')
    grid_quality = models.CharField(max_length=80, null=True, blank=True)
    grid_availability = models.IntegerField(null=True, blank=True, help_text='State in percentage on the average.')
    transformers_detail = models.CharField(max_length=200, null=True, blank=True, help_text='in kVA')
    generators_detail = models.CharField(max_length=200, null=True, blank=True, help_text='in kVA')
    switching_mode = models.CharField(max_length=30, null=True, blank=True)
    minimum_load = models.IntegerField(null=True, blank=True, help_text='kW') 
    average_load = models.IntegerField(null=True, blank=True, help_text='kW') 
    maximum_load = models.IntegerField(null=True, blank=True, help_text='kW') 
    daily_consumption = models.IntegerField(null=True, blank=True, help_text='kWh') 
    


class CommercialIndustryPageTwo(models.Model):
    roof_space_available = models.IntegerField(null=True, blank=True, help_text='square meters') 
    roof_type = models.CharField(max_length=200, null=True, blank=True, help_text='Flat, Mono-Pitch, Double-Pitch, Specify if others')
    roof_material = models.CharField(max_length=30, null=True, blank=True, help_text='Concrete slab, Aluminum, Ardex, Specify if others')
    roofing_sheet_thickness = models.IntegerField(null=True, help_text='if Aluminum')
    roofing_sheet_lapping = models.CharField(max_length=40, null=True, blank=True)
    roofing_truss_material = models.CharField(max_length=40, null=True, blank=True)
    roof_picture = models.ImageField(default='default6.jpg',  upload_to='r_pics')
    ground_space_picture = models.ImageField(default='default7.jpg',  upload_to='gs_pics')
    ground_space_available = models.IntegerField(null=True, blank=True, help_text='square meters') 
    equipment_room_availability = models.BooleanField()
    size_of_equipment_room = models.IntegerField(null=True, blank=True, help_text='square meters')
    ER_picture_or_space_to_build = models.ImageField(default='default8.jpg',  upload_to='er_pics')
    panel_room_picture = models.ImageField(default='default9.jpg',  upload_to='pr_pics')
    roof_to_ER_distance = models.IntegerField(null=True, blank=True, help_text='meters')
    ER_to_power_room_distance = models.IntegerField(null=True, blank=True, help_text='meters')
    pv_genset = models.BooleanField(_("PV-GENSET SOLUTION + GRID"), null=True, blank=True)
    grid_tied = models.BooleanField(_("GRID-TIED SOLUTION"), null=True, blank=True)
    BESS = models.BooleanField(_("BESS SOLUTION"), null=True, blank=True)
    opening_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    closing_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    starsight_rep = models.CharField(_('Starsight Representative'),max_length=50, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    station_rep = models.CharField(_("Station Representative"),max_length=30, null=True, blank=True)
    contact_number = models.CharField(max_length=30, null=True, blank=True)
    comment = models.TextField(_("General Comments"), null=True, blank=True) 

   
class ChecklistForCandI(models.Model):
    page_one = models.OneToOneField("audits.CommercialIndustryPageOne", verbose_name=_("Client Detail | Existing Power and Load Information"), on_delete=models.CASCADE)
    page_two = models.OneToOneField("audits.CommercialIndustryPageTwo", verbose_name=_("Mounting Planes | Equipment Room | Solution Type"), on_delete=models.CASCADE)
   