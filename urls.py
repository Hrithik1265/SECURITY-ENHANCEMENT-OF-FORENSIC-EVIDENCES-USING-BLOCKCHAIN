from django.urls import path

from . import views

urlpatterns = [path("index.html", views.index, name="index"),
			path("AdminLogin", views.AdminLogin, name="AdminLogin"),
			path("PoliceLogin", views.PoliceLogin, name="PoliceLogin"),
			path("HospitalLogin", views.HospitalLogin, name="HospitalLogin"),
			path("UserLogin", views.UserLogin, name="UserLogin"),
			path("Admin.html", views.Admin, name="Admin"),
			path("Hospital.html", views.Hospital, name="Hospital"),
			path("Police.html", views.Police, name="Police"),
			path("User.html", views.User, name="User"),
			path("Download", views.Download, name="Download"),
			path("AddEvidence.html", views.AddEvidence, name="AddEvidence"),
			path("AddEvidenceAction", views.AddEvidenceAction, name="AddEvidenceAction"),
			path("ViewEvidence", views.ViewEvidence, name="ViewEvidence"),
			path("HViewEvidence", views.HViewEvidence, name="HViewEvidence"),
			path("PViewEvidence", views.PViewEvidence, name="PViewEvidence"),
			path("UViewEvidence", views.UViewEvidence, name="UViewEvidence"),
            path("Site1/About.html", views.About,  name="About"),
            path("Site1/Contact.html", views.Contact,  name="Contact"),            
]