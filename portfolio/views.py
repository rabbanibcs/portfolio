from django.shortcuts import render
from .models import Contact,PersonalInfo

# Create your views here.
def index(request):
    info=PersonalInfo.objects.all().first()
    if request.method=="POST":
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        object=Contact(
            email=email,
            subject=subject,
            message=message
        )
        object.save()
        return render(request,"index.html",{
        "message":"Thanks for your concern. We will contact you vey soon.",
        "info":info})
    return render(request,"index.html",{
        "info":info
    })

