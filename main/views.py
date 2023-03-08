from django.shortcuts import redirect, render
from main.filter import LoanFilter

from main.form import ClientForm, LoanForm, SendSMSForm
from main.models import Client, Loan
from django.contrib import messages
from . import send_sms

import requests
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from decouple import config
from django.contrib.auth.decorators import login_required 
from BeemAfrica import Authorize, AirTime, OTP, SMS
Authorize(config("BEEM_API_KEY"), config("BEEM_SECRET_KEY"))

# Create your views here.

def signup(request):
    
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=email).exists():
            messages.error(request, "User alredy exist")
            return redirect(signup)
        else:
            user = User.objects.create_user(username=email, password=password)
            messages.success(request, "Successfull Registered")
            return redirect(signin)

    return render(request, "main/signup.html")

def signin(request):
    if request.method == "POST":
        email2 = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=email2).exists():
            user = authenticate(username= email2, password = password)
            print(user)
            if user is not None:
                login(request=request, user=user)
                messages.success(request, "Successfull Loged In")
                return redirect("/")
            else:
                messages.error(request, "Something Went Wrong")
                return redirect(signin)
        else:
            messages.error(request, "User Does Not Exist")
            return redirect(signin)
  
    return render(request, "main/signin.html")


def logout_user(request):
    logout(request)
    return redirect(home)


@login_required
def home(request):
    clients = Client.objects.all().count()
    open_loans = Loan.objects.filter(status="Active").count()
    paid_loans = Loan.objects.filter(status="Complited").count()
    loan_amount = sum(loan.loan_amount for loan in Loan.objects.all())
    
    context = {"open_loans": open_loans, "paid_loans": paid_loans, "loan_amount": loan_amount, "clients":clients}  
    return render(request, 'main/home.html', context)

@login_required
def clients(request):
    clients_list = Client.objects.all()
    
    context = {
        "clients": clients_list
    }
    return render(request, 'main/clients.html', context)

@login_required
def add_client(request):
    form = ClientForm
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(clients)
    
    context = {
        "form": form
    }
    return render(request, 'main/add_client.html', context)


@login_required
def loans(request):
    loans_list = Loan.objects.all()
    filter =  LoanFilter
  
   
    #print(response.json())
    if request.method == "GET":
        filter =  LoanFilter(request.GET, queryset=loans_list)
        loans_list = filter.qs

    
    context = {
        "loans": loans_list,
        "filter":filter,
    }
    return render(request, 'main/loans.html', context)

@login_required
def add_loan(request):
    form = LoanForm
    if request.method == "POST":
        form = LoanForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "New Loan Added Successfull")
            return redirect(loans)
        messages.success(request, "Something went Wrong")
        return redirect(loans)


    
    context = {
        "form": form
    }
    
    return render(request, 'main/add_loan.html', context)


def view_loan(request, id):
    loan = Loan.objects.get(id=id)
    number_ = loan.client.phone_number
    message_ = f"Hello You are reminded to pay your debt of {loan.loan_amount}"  
    sms_form = SendSMSForm(
    initial_data = {
        'phone_number': number_,
        'message': message_
        }  
    )
    
    if request.method == "POST" and "send_sms_btn" in request.POST:
        print("inside post...............")
        sms_form = SendSMSForm(request.POST)
        number = request.POST['phone_number']
        message = request.POST['message']
        print("data is", number, message)
        response = SMS.send_sms(message, str(number))
        print(response)
        if response["code"] == 100:
            messages.success(request, "SMS Sent successfull..")
            vv = f"/view_loan/{loan.id}"
            return redirect(vv)
        else:
            messages.error(request, "SMS Was Not Sent..")
            vv = f"/view_loan/{loan.id}"
            return redirect(vv)
        
    
    if request.method == "POST" and "pay" in request.POST:
        amount = int(request.POST["amount"])
        loan_now = loan
        if loan_now.loan_amount < amount:
           messages.success(request, f"Amount: {amount} Tsh is greater than Loan Amount")
           vv = f"/view_loan/{loan.id}"
           return redirect(vv)
        else:
            loan_now.loan_amount = loan_now.loan_amount - amount
            loan_now.save()
            messages.success(request, f"Successfull Paid: {amount} Tsh")
            vv = f"/view_loan/{loan.id}"
            return redirect(vv)
        
        

    context = {
        "loan": loan, "sms_form":sms_form
    }
    
    return render(request, 'main/view_loan.html', context)