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
    name = models.CharField(max_length=50, null=True, verbose_name="Branch Name")
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
        ('Pending Audit', 'Pending Audit'),
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



class Checklist(models.Model):
    client = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=200, blank=True, null=True)
    site_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Site Address")
    site_code = models.PositiveIntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    business_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Business Type")
    contact_person_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Contact Person")
    contact_personPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    vendor = models.CharField(max_length=200, blank=True, null=True)
    auditor_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Auditor's Name")
    auditor_phone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    auditDate = models.DateField(null=True, blank=True, verbose_name="Date of Audit")
    #-------------------------------Air conditioners--------------------------------
    location = models.TextField(_("ACs by Location"), null=True, help_text='Please enter the number of ACs per location.', blank=True)
    split_1 = models.IntegerField(_("Number of 1HP"), null=True, blank=True)
    split_2 = models.IntegerField(_("Number of 1.5HP"), null=True, blank=True)
    split_3 = models.IntegerField(_("Number of 2HP"), null=True, blank=True)
    split_4 = models.IntegerField(_("Number of 2.5HP"), null=True, blank=True)
    standing_unit_1 = models.IntegerField(_("Number of 3HP"), null=True, blank=True)
    standing_unit_2 = models.IntegerField(_("Number of 5HP"), null=True, blank=True)
    standing_unit_3 = models.IntegerField(_("Number of 10HP"), null=True, blank=True)
    comment = models.TextField(_("Comment"), null=True, blank=True)
    #------------------------------Lightings-----------------------------------------
    florescent = models.CharField(max_length=50, null=True, blank=True)
    led = models.CharField(max_length=50, null=True, blank=True)
    halogen = models.CharField(max_length=50, null=True, blank=True)
    energy_saver = models.CharField(max_length=50, null=True, blank=True, verbose_name="Energy Saver Bulb")
    panel_light = models.CharField(max_length=50, null=True, blank=True, verbose_name="Panel Light")
    other_lights = models.CharField(max_length=50, null=True, blank=True, help_text='Please state the power rating in Watts.', verbose_name="Other Light Bulbs")
    #------------------------------Appliance----------------------------------------
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
    card_printer = models.IntegerField(null=True, blank=True, verbose_name="Card Printer")
    time_stamping_machine = models.IntegerField(null=True, blank=True, verbose_name="Timestamping Machine")
    shredder = models.IntegerField(null=True, blank=True)
    sorting_machine = models.IntegerField(null=True, blank=True, verbose_name="Sorting Machine")
    fridge = models.IntegerField(null=True, blank=True)
    mantrap_door = models.IntegerField(null=True, blank=True, verbose_name="Mantrap Door")
    hand_dryer = models.IntegerField(null=True, blank=True, verbose_name="Hand Dryer")
    other_appliances = models.TextField(null=True, blank=True, help_text='Please enter the name and counts of other appliances if exist.', verbose_name="Other Appliances")
   
    #------------------------------------Sources of Power ------------------------------------------------
    connects_to_grid = models.BooleanField(default=False, null=True, blank=True, verbose_name="Is the conneted to the Grid?")
    connects_to_generator = models.BooleanField(default=False, null=True, blank=True, verbose_name="Connects to Generator?")
    connects_to_solar = models.BooleanField(default=False, null=True, blank=True, verbose_name="Connects to Solar?")
    details = models.TextField(null=True, blank=True)
    grid_avg_cost = models.CharField(max_length=60, null=True, blank=True, verbose_name="Monthly Average Cost on Grid")
    diesel_avg_cost = models.CharField(max_length=60, null=True, blank=True, verbose_name="Monthly Average Cost on Diesel")
    gensets_maintenance_avg_cost = models.CharField(max_length=60, null=True, blank=True, verbose_name="Average Cost on Generator Maintenance")
    ac_maintenance_avg_cost = models.CharField(max_length=60, null=True, blank=True, verbose_name="Average Cost on Air Conditioners Maintenance")
    other_cost = models.CharField(max_length=60, null=True, blank=True, verbose_name="Other Associated Cost")
    genset_1 = models.CharField(max_length=60, null=True, blank=True,help_text='In kVA')
    genset_2 = models.CharField(max_length=60, null=True, blank=True)
    genset_3 = models.CharField(max_length=60, null=True, blank=True)
    genset_4 = models.CharField(max_length=60, null=True, blank=True)
    transformer_1 = models.CharField(max_length=60, null=True, blank=True,help_text='In kVA')
    transformer_2 = models.CharField(max_length=60, null=True, blank=True)
    noOfAtm = models.PositiveIntegerField(null=True, blank=True, verbose_name="Number of ATMs")
    otherAtmDetails = models.TextField(null=True, blank=True, verbose_name="Other Details")
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    Monday_to_Friday = models.BooleanField(default=False, null=True, blank=True)
    Monday_to_Saturday = models.BooleanField(default=False, null=True, blank=True)
    Monday_to_Sunday = models.BooleanField(default=False, null=True, blank=True)
    item1 = models.CharField(max_length=100, null=True, blank=True, help_text='State the equipment/appliance name and the rating in kVA in each case. ')
    item2 = models.CharField(max_length=100, null=True, blank=True)
    item3 = models.CharField(max_length=100, null=True, blank=True)
    item4 = models.CharField(max_length=100, null=True, blank=True)
    item5 = models.CharField(max_length=100, null=True, blank=True)
    item6 = models.CharField(max_length=100, null=True, blank=True)
    item7 = models.CharField(max_length=100, null=True, blank=True)
    inverter_1 = models.CharField(max_length=100, null=True, blank=True)
    inverter_2 = models.CharField(max_length=100, null=True, blank=True)
    inverter_3 = models.CharField(max_length=100, null=True, blank=True)
    ups_1 = models.CharField(max_length=100, null=True, blank=True,help_text='In kVA')
    ups_2 = models.CharField(max_length=100, null=True, blank=True)
    ups_3 = models.CharField(max_length=100, null=True, blank=True)
    stabilizer_1 = models.CharField(max_length=100, null=True, blank=True,help_text='In kVA')
    stabilizer_2 = models.CharField(max_length=100, null=True, blank=True)
    battery_bank_1 = models.CharField(max_length=100, null=True, blank=True, help_text='e.g 24 units of 12V 200AH', verbose_name="Battery Bank 1")
    battery_bank_2 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Battery Bank 2")
    battery_bank_3 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Battery Bank 3")
    battery_bank_4 = models.CharField(max_length=100, null=True, blank=True, verbose_name="Battery Bank 4")
    # --------------------------------------Building-----------------------------------------------------
    bungalow = models.BooleanField(default=False, null=True, blank=True)
    one_storey = models.BooleanField(default=False, null=True, blank=True, verbose_name="One Storey")
    two_storey = models.BooleanField(default=False, null=True, blank=True, verbose_name="Two Storey")
    three_storey = models.BooleanField(default=False, null=True, blank=True, verbose_name="Three Storey")
    multi_resident = models.BooleanField(default=False, null=True, blank=True, verbose_name="Multi-Resident")
    multi_commercial = models.BooleanField(default=False, null=True, blank=True, verbose_name="Multi-Commercial")
    mall = models.BooleanField(default=False, null=True, blank=True)
    ownership = models.CharField(max_length=100, null=True, blank=True) 
    picture = models.ImageField(default="default1.jpg", upload_to="building_pics", null=True, blank=True)
    roof_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roof Type")
    roof_picture = models.ImageField(default='default2.jpg', upload_to='roof_pics', null=True, blank=True, verbose_name="Roof Picture")
    roof_length = models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Roof Length")
    roof_width =  models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Roof Width")
    total_area =  models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Total Area")
    number_of_panels = models.PositiveIntegerField(null=True, blank=True, verbose_name="Number of Panels")
    roofing_sheet_material = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Sheet Material")  
    roofing_truss_material = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Truss Material")
    roofing_sheet_thickness = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Sheet Thickness (mm)")  
    roofing_truss_spacing =  models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Roofing Truss Spacing") 
    repair_needed = models.BooleanField(default=False, null=True, blank=True, verbose_name="Does the roof requires repairs?")
    minor_repair = models.BooleanField(default=False, null=True, blank=True, verbose_name="Minor Repair")
    major_repair = models.BooleanField(default=False, null=True, blank=True, verbose_name="Major Repair")
    complete_replacement = models.BooleanField(default=False, null=True, blank=True, verbose_name="Complete Replacement")
    changeover_box_picture = models.ImageField(default='default3.jpg',  upload_to='changeover_pics', null=True, blank=True, verbose_name="Attach picture of the Changeover Box")
    Distribution_board_picture = models.ImageField(default='default4.jpg', upload_to='db_pics', null=True, blank=True, verbose_name="Attach picture of the DB")
    general_comment = models.TextField(null=True, blank=True, verbose_name="Comments")

    # ------------------------------------------------Equipment Room ---------------------------------------------
    er_available = models.BooleanField(default=False, null=True, blank=True, verbose_name="Is Equipment Room Available?")
    space_toBuild = models.CharField(max_length=100, null=True, blank=True, verbose_name="If not, is there space to build one? ")
    on_what_floor = models.CharField(max_length=20, null=True, blank=True, verbose_name="On what floor is the ER or the available space")
    dimension = models.CharField(max_length=30, null=True, blank=True, verbose_name="What is the dimension of the room or space?")
    ER_picture_or_space_to_build = models.ImageField(default='default5.jpg',  upload_to='er_pics', null=True, blank=True, verbose_name="Please attach the picture")
    distance_to_generator = models.CharField(max_length=80, null=True, blank=True, verbose_name="State the distance from the ER to the generator")
    distance_to_powerRoom = models.CharField(max_length=80, null=True, blank=True, verbose_name="State the distance from the  ER to the existing Power Room")
    distance_to_roof = models.CharField(max_length=80, null=True, blank=True, verbose_name="State the distance from the  ER to the roof")
    # -----------------------------------Safety-----------------------------------------------------------
    one = models.CharField( _("Will ladder or scaffolds be required for access to the roof?"),max_length=150, null=True)
    two  = models.CharField(_("Will fall protection be required while working on the roof?"), max_length=150, null=True)
    three  = models.CharField( _("Is there enough access and egress at proposed equipment room?"),max_length=150, null=True)
    four  = models.CharField( _("Does the proposed equipment room has an existing smoke/fire alarm?"), max_length=150, null=True)
    five  = models.CharField( _("Is there enough access and egress at the generator area. If we are dealing with a confined space please state?"), max_length=150, null=True)
    six  = models.CharField( _("Are there existing bund walls/secondary spill contigency arrangement around the diesel storage tank?"), max_length=150, null=True)
    seven  = models.CharField( _("Are there visible signs of oil spillage around the generator area/plinth? Please take date-staped pictures"), max_length=150, null=True)
    eight = models.ImageField(default='default6.jpg', upload_to='safety', null=True, blank=True, verbose_name="Attach the picture")
    nine  = models.CharField(
        _("Are there any overhead power cables that will be a problem for work at height?"), max_length=150, null=True)
    ten  = models.CharField( _("Are there any environmental or safety concerns?"), max_length=150, null=True)  
    
    #-------------------------------------------Sign Off ------------------------------------------
    client_rep = models.CharField(max_length=150, null=True, blank=True, verbose_name="Customer Representative's Name")
    position = models.CharField(max_length=80, null=True, blank=True)
    client_repPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Contact Number")
    email = models.CharField(max_length=100, null=True, blank=True)
    GeneralComment = models.TextField(null=True, blank=True, verbose_name="General Comments")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Checklist For Banks"
    
    def __str__(self):
        if (self.vendor or self.client or self.branch) != None: 
            return f"{self.vendor} | {self.client} | {self.branch}"
        else:
            return "vendor or client or branch field was not filled."
        




class Checklist2(models.Model):
    # -------------------------------------Customer Details --------------------------------------------------------
    client = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=200, blank=True, null=True)
    site_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Site Address")
    site_code = models.PositiveIntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    business_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Business Type")
    contact_person_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Contact Person")
    contact_personPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    vendor = models.CharField(max_length=200, blank=True, null=True)
    auditor_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Auditor's Name")
    auditor_phone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    auditDate = models.DateField(null=True, blank=True, verbose_name="Date of Audit")
    # ----------------------------- Pumps and Air Conditioners----------------------------------------------------------
    pms_pump = models.CharField(max_length=100, null=True, blank=True, verbose_name="Number and Size(in HP) of PMS Pumps")   
    ago_pump = models.CharField(max_length=100, null=True, blank=True, verbose_name="Number and Size(in HP) of AGO Pumps")   
    dpk_pump = models.CharField(max_length=100, null=True, blank=True, verbose_name="Number and Size(in HP) of DPK Pumps")  
    surface_transfer_pump = models.CharField(max_length=100, null=True, blank=True, verbose_name="Size (in HP) of the surface pumps")   
    water_pump = models.CharField(max_length=100, null=True, blank=True, verbose_name="Water Pumps")   
    location = models.TextField(_("ACs by Location"), null=True, blank=True, help_text='Please enter the number of ACs by location, stating the codition as: working or not working.')
    split_1 = models.IntegerField(_("Number of 1HP"), null=True, blank=True) 
    split_2 = models.IntegerField(_("Number of 1.5HP"), null=True, blank=True)
    split_3 = models.IntegerField(_("Number of 2HP"), null=True, blank=True)
    split_4 = models.IntegerField(_("Number of 2.5HP"), null=True, blank=True)
    standing_unit_1 = models.IntegerField(_("Number of 3HP"), null=True, blank=True)
    standing_unit_2 = models.IntegerField(_("Number of 5HP"), null=True, blank=True)
    standing_unit_3 = models.IntegerField(_("Number of 10HP"), null=True, blank=True)

    #page 2
    #-------------------------------------------Lightings-----------------------------------------------------------------------
    florescent = models.CharField(max_length=50, null=True, blank=True)
    led = models.CharField(max_length=50, null=True, blank=True)
    halogen = models.CharField(max_length=50, null=True, blank=True)
    energy_saver = models.CharField(max_length=50, null=True, blank=True, verbose_name="Energy Saver Bulb")
    panel_light = models.CharField(max_length=50, null=True, blank=True, verbose_name="Panel Light")
    other_lights = models.CharField(max_length=50, null=True, blank=True, help_text='Please state the power rating in Watts.', verbose_name="Other Light Bulbs")
    #------------------------------Generators-----------------------------------------------------------------------------------
    generator_1 = models.CharField(max_length=50, null=True, blank=True, help_text="in kVA")
    generator_2 = models.CharField(max_length=50, null=True, blank=True)
    connects_to_grid = models.CharField(max_length=50, null=True, blank=True)
    transformer_size = models.CharField(max_length=50, null=True, blank=True, help_text="in kVA") 
    # ---------------------------------------Electrical Appliances---------------------------------------------------------
    fridge = models.IntegerField(null=True, blank=True)
    freezer = models.IntegerField(null=True, blank=True)
    fan = models.IntegerField(null=True, blank=True)
    printer = models.IntegerField(null=True, blank=True)
    scanner = models.IntegerField(null=True, blank=True)
    note_counting_machine = models.IntegerField(null=True, blank=True, verbose_name="Note Counting Machine")
    others_equipment = models.TextField(verbose_name="Other Equipment")
    
    three_phase_equipment = models.BooleanField( verbose_name="I there any 3- Phase Equipment?")
    size = models.CharField(max_length=100, null=True, blank=True,help_text='State the size of te three pahse equipment (in HP)')
    # ---------------------------------------Building----------------------------------------------------------------
    #page 3
    roof_type = models.CharField(max_length=200, null=True, blank=True, help_text='Flat, Mono-Pitch, Double-Pitch, Specify if others', verbose_name="Roof Type")
    roof_material = models.CharField(max_length=30, null=True, blank=True, help_text='Concrete slab, Aluminum, Ardex, Specify if others', verbose_name="Roof Material")
    roofing_sheet_material = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Sheet Material")  
    roofing_truss_material = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Truss Material") 
    roofing_sheet_thickness = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Sheet Thickness (mm)") 
    roofing_truss_spacing =  models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Roofing Truss Spacing")   
    ER_picture_or_space_to_build = models.ImageField(default='default1.jpg',  upload_to='er_pics', null=True, blank=True, verbose_name="Please attach the picture")
    building_type = models.CharField(max_length=100, default=False, help_text='State the building type and other information as below.', verbose_name="Building Type")
    building_picture = models.ImageField(default='default2.jpg',  upload_to='building_pics', verbose_name="Attach picture of the building")
    roof_picture = models.ImageField(default='default3.jpg', upload_to='roof_pics', null=True, blank=True, verbose_name="Roof Picture")
    changeover_box_picture = models.ImageField(default='default4.jpg',  upload_to='changeover_pics', null=True, blank=True, verbose_name="Attach picture of the Changeover Box")
    Distribution_board_picture = models.ImageField(default='default5.jpg', upload_to='db_pics', null=True, blank=True, verbose_name="Attach picture of the DB")
    opening_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    closing_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    # -----------------------------------Safety-----------------------------------------------------------
    one = models.CharField( _("Will ladder or scaffolds be required for access to the roof?"),max_length=150, null=True)
    two  = models.CharField(_("Will fall protection be required while working on the roof?"), max_length=150, null=True)
    three  = models.CharField( _("Is there enough access and egress at proposed equipment room?"),max_length=150, null=True)
    four  = models.CharField( _("Does the proposed equipment room has an existing smoke/fire alarm?"), max_length=150, null=True)
    five  = models.CharField( _("Is there enough access and egress at the generator area. If we are dealing with a confined space please state?"), max_length=150, null=True)
    six  = models.CharField( _("Are there existing bund walls/secondary spill contigency arrangement around the diesel storage tank?"), max_length=150, null=True)
    seven  = models.CharField( _("Are there visible signs of oil spillage around the generator area/plinth? Please take date-staped pictures"), max_length=150, null=True)
    eight = models.ImageField(default='default6.jpg', upload_to='safety', null=True, blank=True, verbose_name="Attach the picture")
    nine  = models.CharField(
        _("Are there any overhead power cables that will be a problem for work at height?"), max_length=150, null=True)
    ten  = models.CharField( _("Are there any environmental or safety concerns?"), max_length=150, null=True)  
    
    #-------------------------------------------Sign Off ------------------------------------------
    client_rep = models.CharField(max_length=150, null=True, blank=True, verbose_name="Customer Representative's Name")
    position = models.CharField(max_length=80, null=True, blank=True)
    client_repPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Contact Number")
    email = models.CharField(max_length=100, null=True, blank=True)
    GeneralComment = models.TextField(null=True, blank=True, verbose_name="General Comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Checklist For Gas and Fuel Stations"
    
    def __str__(self):
        if (self.vendor or self.client or self.branch) != None: 
            return f"{self.vendor} | {self.client} | {self.branch}"
        else:
            return "vendor or client or branch field was not filled."
   


   
class Checklist3(models.Model):
    # -------------------------------------Customer Details --------------------------------------------------------
    client = models.CharField(max_length=200, blank=True, null=True)
    branch = models.CharField(max_length=200, blank=True, null=True)
    site_address = models.CharField(max_length=200, null=True, blank=True, verbose_name="Site Address")
    site_code = models.PositiveIntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True)
    business_type = models.CharField(max_length=100, null=True, blank=True, verbose_name="Business Type")
    contact_person_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Contact Person")
    contact_personPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    vendor = models.CharField(max_length=200, blank=True, null=True)
    auditor_name = models.CharField(max_length=200, null=True, blank=True, verbose_name="Auditor's Name")
    auditor_phone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Phone")
    auditDate = models.DateField(null=True, blank=True, verbose_name="Date of Audit")
    # -------------------------------Grid Details-------------------------------------------------------------------  
    connects_to_grid = models.BooleanField(default=False, null=True, blank=True, verbose_name="Is the Facility conneted to the Grid?")
    reasons = models.CharField(max_length=200, null=True, blank=True, help_text="If not connected, state reasons.")
    grid_quality = models.CharField(max_length=80, null=True, blank=True, verbose_name="Grid Quality")
    grid_availability = models.IntegerField(null=True, blank=True, help_text='How many hours out of 24 do you get on an average?', verbose_name="Grid Availability")
    day = models.PositiveIntegerField()
    night = models.PositiveIntegerField()
    transformer_1 = models.CharField(max_length=100, null=True, blank=True,help_text='State the type(step up/down), Breaker Size, location and the rating In kVA for each')
    transformer_2 = models.CharField(max_length=100, null=True, blank=True)
    transformer_3 = models.CharField(max_length=100, null=True, blank=True)
    transformer_4 = models.CharField(max_length=100, null=True, blank=True)
    transformer_5 = models.CharField(max_length=100, null=True, blank=True)
    transformer_6 = models.CharField(max_length=100, null=True, blank=True)
    transformer_7 = models.CharField(max_length=100, null=True, blank=True)
    transformer_8 = models.CharField(max_length=100, null=True, blank=True)
    transformer_9 = models.CharField(max_length=100, null=True, blank=True)
    transformer_10 = models.CharField(max_length=100, null=True, blank=True)
    tariff = models.CharField(max_length=100, null=True, blank=True, help_text='cost per kWh')
    # ----------------------------------------Generator Details------------------------------------------------------
    genset_1 = models.CharField(max_length=60, null=True, blank=True,help_text='State the type (GG or GG), Make, Ownership, Engine Run-Hour, Breaker Size, Controller Type&Model, location and the rating in kVA or kW for each')
    genset_2 = models.CharField(max_length=60, null=True, blank=True)
    genset_3 = models.CharField(max_length=60, null=True, blank=True)
    genset_4 = models.CharField(max_length=60, null=True, blank=True)
    genset_5 = models.CharField(max_length=60, null=True, blank=True)
    genset_6 = models.CharField(max_length=60, null=True, blank=True)
    #  Page 2
    # ------------------------------------Power Euipment---------------------------------------------- 
    switching_mode = models.CharField(max_length=30, null=True, blank=True, verbose_name="Whta is the mode of Switching Power?")
    availability_of_synchPanel = models.BooleanField(default=False, blank=True, verbose_name="Is there a Synchronization Panel?")
    synchPanelSize = models.CharField(max_length=200, null=True, blank=True, verbose_name="What Voltage Level is the Panel?")
    spareBreaker = models.BooleanField(null=True, blank=True, verbose_name="Is there a Spare Breaker at the Injection Point?")
    breakerSize = models.CharField(max_length=100, null=True, blank=True, verbose_name="Is there a Spare Breaker at the Injection Point?")
    
    # -------------------------------------------Load Details-------------------------------------------
    minimum_load = models.CharField(max_length=30,null=True, blank=True, help_text='kW',verbose_name="Minimum Load") 
    average_dayLoad = models.CharField(max_length=30,null=True, blank=True, help_text='kW', verbose_name="Average Load") 
    average_nightLoad = models.CharField(max_length=30,null=True, blank=True, help_text='kW', verbose_name="Average Night Load") 
    maximum_load = models.CharField(max_length=30,null=True, blank=True, help_text='kW', verbose_name="Maximum Load") 
    daily_consumption = models.CharField(max_length=30,null=True, blank=True, help_text='kWh', verbose_name="Average Daily Energy Consumption") 
    #------------------------------------------Bacup System------------------------------------------
    backupSize = models.DecimalField(max_digits=12, decimal_places=10, null=True, blank=True, verbose_name="Size of Critical Load (kW)")
    # ------------------------------Building and Mounting Planes----------------------------------------
    building_type = models.CharField(max_length=100, default=False, help_text='State the building type and other information as below.', verbose_name="Building Type")
    roof_space_1 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Roof Space 1")
    roof_space_2 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Roof Space 2")
    roof_space_3 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Roof Space 3")
    roof_space_4 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Roof Space 4")
    roofing_truss_material = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Truss Material")  
    roofing_sheet_thickness = models.CharField(max_length=100, null=True, blank=True, verbose_name="Roofing Sheet Thickness (mm)")
    roofing_truss_spacing =  models.DecimalField(max_digits=8, decimal_places=4, null=True, verbose_name="Roofing Truss Spacing")
    roof_picture = models.ImageField(default='default1.jpg', upload_to='roof_pics', null=True, blank=True, verbose_name="Roof Picture")
    ground_space_1 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Ground Space 1")
    ground_space_2 = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Ground Space 2")
    ground_space_picture = models.ImageField(default='default2.jpg',  upload_to='gs_pics', verbose_name="Attach picture of the Ground Space")
    #---------------------------------- Equipment Room------------------------------------
    equipment_room_availability = models.BooleanField(verbose_name="Is Equipment Room Available?")
    size_of_equipment_room = models.IntegerField(null=True, blank=True, help_text='square meters', verbose_name="Size of Equipment Room")
    ER_picture_or_space_to_build = models.ImageField(default='default3.jpg',  upload_to='er_pics', verbose_name="Please attach the picture")
    distance_to_generator = models.CharField(max_length=80, null=True, blank=True, verbose_name="State the distance from the ER to the generator")
    panel_room_picture = models.ImageField(default='default4.jpg',  upload_to='pr_pics', verbose_name="Existing Power Room Picture")
    roof_to_ER_distance = models.IntegerField(null=True, blank=True, help_text='meters', verbose_name="State the distance from the  ER to the roof")
    ER_to_power_room_distance = models.IntegerField(null=True, blank=True, help_text='meters', verbose_name="State the distance from the  ER to the existing Power Room")
    #------------------------------------------Operation Hour--------------------------
    opening_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    closing_time = models.TimeField(null=True, blank=True, help_text='State in 24-hours format')
    #------------------------------------------Sign Off--------------------------
    client_rep = models.CharField(max_length=150, null=True, blank=True, verbose_name="Customer Representative's Name")
    position = models.CharField(max_length=80, null=True, blank=True)
    client_repPhone = models.PositiveIntegerField(null=True, blank=True, verbose_name="Contact Number")
    email = models.CharField(max_length=100, null=True, blank=True)
    GeneralComment = models.TextField(null=True, blank=True, verbose_name="General Comments")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Checklist For C&I"
    
    def __str__(self):
        if (self.vendor or self.client or self.branch) != None: 
            return f"{self.vendor} | {self.client} | {self.branch}"
        else:
            return "vendor or client or branch field was not filled."


