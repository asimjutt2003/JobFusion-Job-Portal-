from django.urls import path
from . import views

urlpatterns = [
    path("", views.CandIndexPage, name="Index"),
    path("CompanyIndex/", views.ComIndexPage, name="CompanyIndex"),
    path("signup/", views.SignupPage, name="signup"),
    path("register/", views.RegisterUser, name="register"),
    path("otppage/", views.OTPPage, name="otppage"), 
    path("otp/", views.OtpVerify, name="otp"),
    path("loginpage/", views.Loginpage, name="loginpage"),
    path("loginuser/", views.Loginuser, name="login"),
    path("profile/<int:pk>", views.ProfilePage, name="profile"),
    path("updateprofile/<int:pk>", views.UpdateProfile, name="updateprofiles"),
    path("findjob/", views.FindJob, name="findjob"),
    path("jobsingle/", views.JobDetail, name="jobsingle"),
    path("jobpost/", views.JobPost, name="jobpost"),
    path("jobpostpage/", views.JobDetailSubmit, name="jobpostpage"),



    path("companyindex/", views.postjoblist, name="companyindex"),
    path("companylogout/", views.Companylogout, name="companylogout"),
    path("jobapply/<int:pk>", views.Apply, name="jobapply"),
    path("apply/<int:pk>", views.ApplyJobs, name="apply"),
    path("jobapplylist/", views.JobApplyList, name="jobapplylist"),




    ###### EXTRA URL
    path("blogpage/", views.BlogView, name="blogpage"),
    path("aboutpage/", views.AboutView, name="aboutpage"),
    path("servicepage/", views.ServiceView, name="servicepage"),
    path("servicesingle/", views.Service2View, name="servicesingle"),
    path("testimonials/", views.testimonials, name="testimonials"),
    path("faq/", views.FAQ, name="faq"),
    path("gallery/", views.Gallery, name="gallery"),
    path("contact/", views.Contact, name="contact"),
]