from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Complaint, Departments
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as userLogin, logout as userLogout
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def HOME(request):
    return render(request,'index.html')

def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['pass']
        user = authenticate(username=username, password=password)
        if user is not None:
            userLogin(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password Didn't Match ")
            return render(request,'Memberlogin.html')
    return render(request,'Memberlogin.html')

@login_required(login_url='login')
def complaint(request):
    if request.POST:
        print(request.POST)
        complaint = Complaint.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            contact = request.POST['contact'],
            complaint = request.POST['complaint'],
            file = request.FILES['files'],
            created_by = request.user.id,
            department_id = request.POST['department']
        )
        
        complain_context = {
            'name': complaint.name,
            'email': complaint.email,
            'contact': complaint.contact,
            'complaint': complaint.complaint,
        }
        ownerMail = []
        ownerMail.append(settings.EMAIL_HOST_USER)
        ownerMail.append(complaint.email)
        msg = EmailMessage(f'New Complaint', render_to_string(
        'mail.html', complain_context), settings.EMAIL_HOST_USER, ownerMail)
        msg.content_subtype = "html"
        msg.attach_file(f'{complaint.file}')
        msg.send()
        return redirect('thankyou')
    department = Departments.objects.all()
    return render(request,  'complaint_form.html', {'department': department})



@login_required(login_url='login')
def thankyou(request):
    return render(request,  'thankyou.html')

@login_required(login_url='login')
def logout(request):
    userLogout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        email = request.POST['email']

        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username Already Taken')
            return render(request,  'memberregister.html')
        else:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, 'Registered Successfully')
    return render(request,  'memberregister.html')

@login_required(login_url='login')
def mycomplaints(request):
    complaint_list = Complaint.objects.filter(created_by = request.user.id)
    p = Paginator(complaint_list, 10)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    context = {'page_obj': page_obj}
    return render(request,  'mycomplaints.html',context)