from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.validators import validate_email
from .models import Usermaster, Candidate, Company, Postjob
from random import randint


def CandIndexPage(request):
    return render(request, "app/index.html")

def ComIndexPage(request):
    return render(request, "app/company/index.html")


def SignupPage(request):
    return render(request, "app/login.html")

def RegisterUser(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        # Initialize an empty error message
        message = None

        # Validate all inputs
        if not fname:
            message = "Firstname is Missing"
        elif not lname:
            message = "Lastname is Missing"
        elif not email:
            message = "Email is Missing"
        elif not role or role == 'role':
            message = "Select a Role"
        elif password != cpassword:
            message = "Passwords do not match"
        elif Usermaster.objects.filter(email=email).exists():
            message = "An account already exists with this email"

        if message:
            # If there's an error, render the form with the entered data and the error message
            context = {
                'registration_msg': message,
                'role': role,
                'firstname': fname,
                'lastname': lname,
                'email': email
            }
            return render(request, "app/login.html", context)

        # Create user and specific role details
        otp = randint(100000, 999999)
        newuser = Usermaster.objects.create(role=role, otp=otp, email=email, password=password)  # Store password as plain text

        if role == "Candidate":
            Candidate.objects.create(user_id=newuser, firstname=fname, lastname=lname)
        elif role == "Company":
            Company.objects.create(user_id=newuser, firstname=fname, lastname=lname)
        else:
            message = "Invalid role specified"
            return render(request, "app/login.html", {'registration_msg': message})

        return render(request, "app/otpverify.html", {'email': email})

    return render(request, "app/login.html")





def OTPPage(request):
    return render(request, "app/otpverify.html")


def OtpVerify(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = int(request.POST.get('otp', 0))

        try:
            user = Usermaster.objects.get(email=email)
            if user.otp == otp:
                message = "OTP Verify Successfully"
                return render(request, "app/login.html", {'msg': message})
            else:
                message = "Invalid OTP"
                return render(request, "app/otpverify.html", {'msg': message})
        except Usermaster.DoesNotExist:
            return render(request, "app/login.html", {'msg': "User not found"})

    return redirect('OTPPage')


def Loginpage(request):
    return render(request, "app/login.html")


def Loginuser(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Usermaster.objects.get(email=email)
            if user.password == password:
                if (role == "Candidate" and user.role == "Candidate"):
                    profile = Candidate.objects.get(user_id=user)
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = profile.firstname
                    request.session['lastname'] = profile.lastname
                    request.session['email'] = user.email
                    return render(request, "app/index.html")
                elif(role == "Company" and user.role == "Company"):
                    profile = Company.objects.get(user_id=user)
                    request.session['id'] = user.id
                    request.session['role'] = user.role
                    request.session['firstname'] = profile.firstname
                    request.session['lastname'] = profile.lastname
                    request.session['email'] = user.email
                    return render(request, "app/company/index.html")
                else:
                    message = "Role does not match"
            else:
                message = "Password does not match"
        except Usermaster.DoesNotExist:
            message = "User not found"

        return render(request, "app/login.html", {'login_msg': message})

    return render(request, "app/login.html")



def ProfilePage(request, pk):
    user = get_object_or_404(Usermaster, pk=pk)

    if user.role == "Candidate":
        profile = get_object_or_404(Candidate, user_id=user)
        return render(request, "app/profile.html", {'user': user, 'profile': profile, 'role': 'Candidate'})

    elif user.role == "Company":
        profile = get_object_or_404(Company, user_id=user)
        return render(request, "app/profile.html", {'user': user, 'profile': profile, 'role': 'Company'})

    else:
        return render(request, "app/profile.html", {'user': user, 'role': 'Unknown'})


def UpdateProfile(request, pk):
    user = get_object_or_404(Usermaster, pk=pk)

    if request.method == 'POST':
        if user.role == "Candidate":
            profile = get_object_or_404(Candidate, user_id=user)
            profile.state = request.POST.get('state', profile.state)
            profile.city = request.POST.get('city', profile.city)
            profile.address = request.POST.get('address', profile.address)
            profile.contact = request.POST.get('contact', profile.contact)
            profile.gender = request.POST.get('gender', profile.gender)
            profile.dob = request.POST.get('dob', profile.dob)
            if 'image' in request.FILES:
                profile.profile_pic = request.FILES['image']

        elif user.role == "Company":
            profile = get_object_or_404(Company, user_id=user)
            profile.state = request.POST.get('state', profile.state)
            profile.city = request.POST.get('city', profile.city)
            profile.address = request.POST.get('address', profile.address)
            profile.contact = request.POST.get('contact', profile.contact)
            profile.company_name = request.POST.get('company_name', profile.company_name)
            if 'image' in request.FILES:
                profile.logo_pic = request.FILES['image']

        profile.save()
        return redirect(f'/profile/{pk}')
    else:
        raise PermissionDenied("Invalid request method.")


def JobDetail(request):
    return render(request, "app/job-single.html")


def JobPost(request):
    return render(request, "app/postjob.html")


from django.shortcuts import render, redirect, get_object_or_404
from .models import Usermaster, Company, Postjob
from django.core.exceptions import ValidationError

def JobDetailSubmit(request):
    if request.method == 'POST':
        user_id = request.session.get('id')
        if not user_id:
            return redirect('Loginpage')

        user = get_object_or_404(Usermaster, id=user_id)
        if user.role == "Company":
            comp = get_object_or_404(Company, user_id=user)
            jobname = request.POST.get('jobname', '').strip()
            companyname = request.POST.get('companyname', '').strip()
            companyaddress = request.POST.get('companyaddress', '').strip()
            jobdescription = request.POST.get('jobdescription', '').strip()
            qualification = request.POST.get('qualification', '').strip()
            location = request.POST.get('location', '').strip()
            responsibilities = request.POST.get('responsibilities', '').strip()
            companywebsite = request.POST.get('companywebsite', '').strip()
            companyemail = request.POST.get('companyemail', '').strip()
            companycontact = request.POST.get('companycontact', '').strip()
            salarypackage = request.POST.get('salarypackage', '').strip()
            logo_pic = request.FILES.get('image', None)

            experiences = request.POST.get('experiences', '').strip()
            try:
                experiences = int(experiences)  # Convert to integer, or handle as needed
            except ValueError:
                experiences = None

            # Check for required fields
            if not jobname:
                return render(request, "app/postjob.html", {
                    'error_msg': 'Job Title is required',
                    'form_data': request.POST
                })
            if not companyname:
                return render(request, "app/postjob.html", {
                    'error_msg': 'Company Name is required',
                    'form_data': request.POST
                })
            if not qualification:
                return render(request, "app/postjob.html", {
                    'error_msg': 'Qualification is required',
                    'form_data': request.POST
                })
            if not salarypackage:
                return render(request, "app/postjob.html", {
                    'error_msg': 'Salary Package is required',
                    'form_data': request.POST
                })

            # Check if experiences is None and handle accordingly
            if experiences is None:
                return render(request, "app/postjob.html", {
                    'error_msg': 'Experience must be a valid number',
                    'form_data': request.POST
                })

            Postjob.objects.create(
                company_id=comp,
                jobnames=jobname,
                companynames=companyname,
                companyaddresss=companyaddress,
                jobdescriptions=jobdescription,
                qualifications=qualification,
                resposibiltiess=responsibilities,
                locations=location,
                companywebsites=companywebsite,
                companyemails=companyemail,
                companycontacts=companycontact,
                salarypackages=salarypackage,
                experiences=experiences,
                logo_pic=logo_pic
            )

            message = "Job Posted Successfully"
            return render(request, "app/postjob.html", {'msg': message})

    return redirect('jobpost')







def postjoblist(request):
    all_job = Postjob.objects.all()
    return render(request, "app/company/postjoblist.html",{'all_job':all_job})


def FindJob(request):
    all_job = Postjob.objects.all()
    return render(request, "app/find-job.html",{'all_job':all_job})



from django.shortcuts import redirect

def Companylogout(request):
    # Check if 'email' is in session and delete it
    if 'email' in request.session:
        del request.session['email']
        
    # Check if 'password' is in session and delete it
    if 'password' in request.session:
        del request.session['password']
        
    return redirect('loginpage')


def Apply(request, pk):
    user = request.session.get('id')
    if user:
        cand = Candidate.objects.get(user_id=user)
        job = Postjob.objects.get(id=pk)

        return render(request, "app/apply.html", {'user': user,'cand':cand, 'job': job})
    else:
        # Handle the case where the user is not logged in or session is not set
        return render(request, "app/error.html", {"msg": "You must be logged in to apply for a job."})

from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from .models import Candidate, Postjob, ApplyJob

def ApplyJobs(request, pk):
    try:
        user_id = request.session.get('id')
        if not user_id:
            return render(request, "app/login.html", {'error': 'Please log in to apply for a job.'})
        
        can = get_object_or_404(Candidate, user_id=user_id)
        job = get_object_or_404(Postjob, id=pk)

        if request.method == 'POST':
            salary = request.POST.get('salary')
            gender = request.POST.get('gender')
            resume = request.FILES.get('resume')  # Correctly access uploaded file
            experiences = request.FILES.get('experiences')
            jobname = request.FILES.get('jobname')

            if not salary or not gender or not resume:
                return render(request, "app/apply.html", {
                    'cand': can,
                    'job': job,
                    'msg': 'Upload Required Files',
                    'error': 'Resume is a required field.'
                })

            ApplyJob.objects.create(
                candidate=can,
                job=job,
                Salary=salary,
                gender=gender,
                resume=resume
            )

            message = "Job Applied Successfully"
            return render(request, "app/apply.html", {'msg': message, 'cand': can, 'job': job})

        else:
            return render(request, "app/apply.html", {'cand': can, 'job': job})

    except ObjectDoesNotExist:
        return render(request, "app/error.html", {'error': 'Candidate or job not found.'})
    except Exception as e:
        return render(request, "app/error.html", {'error': str(e)})



def JobApplyList(request):
    all_jobapply = ApplyJob.objects.all()
    return render(request,"app/company/appjoblist.html",{'all_job':all_jobapply})


####### EXTRA VIEWS


def BlogView(request):
    return render(request, "app/blog.html")

def AboutView(request):
    return render(request, "app/about.html")
def ServiceView(request):
    return render(request, "app/services.html")
def Service2View(request):
    return render(request, "app/service-single.html")
def testimonials(request):
    return render(request, "app/testimonials.html")
def FAQ(request):
    return render(request, "app/faq.html")
def Gallery(request):
    return render(request, "app/gallery.html")
def Contact(request):
    return render(request, "app/contact.html")