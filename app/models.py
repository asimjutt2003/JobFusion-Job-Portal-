from django.db import models

# Create your models here.

class Usermaster(models.Model):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
    otp = models.IntegerField()
    role = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_created = models.DateTimeField(auto_now_add=True)
    is_updated = models.DateTimeField(auto_now=True)


class Candidate(models.Model):
    user_id = models.ForeignKey(Usermaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    # skill_level = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    dob = models.CharField(max_length=50)   
    gender = models.CharField(max_length=50)
    # experience = models.CharField(max_length=50, default="0 years")    
    # website = models.CharField(max_length=50)  
    # linkedin = models.CharField(max_length=50)   
    profile_pic = models.ImageField(upload_to="app/img/candidate")

class Company(models.Model):
    user_id = models.ForeignKey(Usermaster, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    company_name = models.CharField(max_length=150)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    logo_pic = models.ImageField(upload_to="app/img/company")


class Postjob(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    jobnames = models.CharField(max_length=250)
    companynames = models.CharField(max_length=250)
    companyaddresss = models.CharField(max_length=250)
    jobdescriptions = models.CharField(max_length=500)
    qualifications = models.CharField(max_length=250)
    resposibiltiess = models.CharField(max_length=250)
    locations = models.CharField(max_length=250)
    companywebsites = models.CharField(max_length=250)
    companyemails = models.CharField(max_length=250)
    companycontacts = models.CharField(max_length=250)
    salarypackages = models.CharField(max_length=250)
    experiences = models.IntegerField()
    logo_pic = models.ImageField(upload_to="app/joblogo",default=0)
    


class ApplyJob(models.Model):
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE)
    job = models.ForeignKey(Postjob,on_delete=models.CASCADE)
    Salary = models.CharField(max_length=200)
    resume = models.FileField(upload_to="app/resume")
    gender = models.CharField(max_length=200)
    experiences = models.IntegerField(default=0)
    jobname = models.CharField(max_length=250,default=0)
    location = models.CharField(max_length=250,default=0)