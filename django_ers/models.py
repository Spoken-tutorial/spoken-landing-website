from django.db import models

# Create your models here.
EVENT_TYPE = [
    ('JOB','JobFair'),
    ('INTERN','Internship')
]
class Event(models.Model):
    name = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    logo = models.FileField(upload_to='brochures')
    type = models.CharField(max_length=200,choices=EVENT_TYPE,default="JOB")
    status = models.BooleanField(default=True) # if inactive , it will not be made public
    show_on_homepage = models.BooleanField(default=True)
    description = models.TextField(blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'events_event'

    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=200)
    # emp_name = models.CharField(max_length=200,verbose_name="Company HR Representative Name") #Name of the company representative
    # emp_contact = models.CharField(validators=[phone_regex], max_length=17,verbose_name="Phone Number")
    # state_c = models.IntegerField(null=True,verbose_name='State (Company Headquarters)',blank=True)
    # city_c = models.IntegerField(null=True,verbose_name='City (Company Headquarters)',blank=True)    
    # address = models.CharField(max_length=250) #Company Address for correspondence
    # email = models.EmailField(null=True,blank=True) #Email for correspondence
    # logo = models.ImageField(upload_to='logo/',null=True,blank=True)
    # description = models.TextField(null=True,blank=True,verbose_name="Description about the company")
    # domain = models.ForeignKey(Domain,on_delete=models.CASCADE) #Domain od work Eg. Consultancy, Development, Software etc
    # company_size = models.CharField(max_length=25,choices=NUM_OF_EMPS,default=DEFAULT_NUM_EMP) #Number of employees in company
    website = models.URLField(null=True,blank=True)
    # date_created = models.DateTimeField(auto_now_add=True)
    # date_updated = models.DateTimeField(auto_now=True )
    # status = models.BooleanField(default=True)
    # added_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    # slug = models.SlugField(max_length = 250, null = True, blank = True)
    # rating = models.IntegerField(null=True,blank=True,verbose_name="Visibility")

    def __str__(self):
        return self.name




class Job(models.Model):
    title = models.CharField(max_length=250,verbose_name="Title of the job page") #filter
    designation = models.CharField(max_length=250,verbose_name='Designation (Job Position)') 
    state_job = models.IntegerField(null=False,blank=False)  #spk #filter
    city_job = models.IntegerField(null=False,blank=False)  #spk #filter
    company=models.ForeignKey(Company,null=True,on_delete=models.CASCADE)
    # skills = models.CharField(max_length=400,null=True,blank=True) 
    description = models.TextField(null=True,blank=True,verbose_name="Job Description") 
    # domain = models.ForeignKey(Domain,on_delete=models.CASCADE,verbose_name='Job Sector') #Domain od work Eg. Consultancy, Development, Software etc
    # salary_range_min = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Minimum)')
    # salary_range_max = models.IntegerField(null=True,blank=True,verbose_name='Annual Salary (Maximum)')
    # date_created = models.DateTimeField(auto_now_add=True,null = True, blank = True)
    # date_updated = models.DateTimeField(auto_now=True,null = True, blank = True )
    # job_type = models.ForeignKey(JobType,on_delete=models.CASCADE)
    # 0: Job is inactive(added but not visible to students)
    # 1: Job is active(added & available to students for apply)
    # 2: Job Application Date is over
    # 3: Job Application is in process with HR & Company
    # 4: Student selected & job closed.
    # status = models.IntegerField(default=1,blank=True)
    # requirements = models.TextField(null=True,blank=True,verbose_name="Qualifications/Skills Required") #Educational qualifications, other criteria
    # shift_time = models.CharField(max_length=200,blank=True)
    # key_job_responsibilities = models.TextField(null=True,blank=True,verbose_name="Key Job Responsibilities")
    # gender = models.CharField(max_length=10,choices=GENDER,default='a')
    
    # slug = models.SlugField(max_length = 250, null = True, blank = True)
    # last_app_date = models.DateTimeField(verbose_name="Last Application Date")
    # rating = models.IntegerField(null=True,blank=True,verbose_name="Visibility")
    # foss = models.CharField(max_length=200)
    # # institute_type = models.CharField(max_length=200,null=True,blank=True)
    # institute_type = models.CharField(max_length=200,blank=True)
    # # state = models.CharField(max_length=200,null=True,blank=True)
    # state = models.CharField(max_length=200,blank=True)
    # # city = models.CharField(max_length=200,null=True,blank=True)
    # city = models.CharField(max_length=200,blank=True)
    # grade = models.IntegerField()
    # activation_status = models.IntegerField(max_length=10,choices=ACTIVATION_STATUS,blank=True,null=True)
    # from_date = models.DateField(null=True,blank=True,verbose_name='Test Date From')
    # to_date = models.DateField(null=True,blank=True,verbose_name='Test Date Upto')
    # num_vacancies = models.IntegerField(default=1,blank=True)
    # degree = models.ManyToManyField(Degree,blank=True,related_name='degrees')
    # discipline = models.ManyToManyField(Discipline,blank=True,related_name='disciplines')
    # job_foss = models.ManyToManyField(Foss,null=True,blank=True,related_name='fosses')
    def __str__(self):
        return self.title



