import random
from django.shortcuts import render ,redirect
from .task import handle_calculation
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm , LoginForm
from django.core.mail import send_mail ,EmailMessage
from django.utils.timezone import now
from django.http import JsonResponse
from django.contrib import messages
from .otp import genrate_otp
from .models import Arithmatic
# Create your views here.

def signup(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add')
    return render(request, 'myapp/signup.html', {'form': form})

def signin(request):
    form = LoginForm(request, data=request.POST or None) 

    if request.method == "POST":
        if "generate_otp" in request.POST:
            otp = genrate_otp()
            request.session["otp"] = otp  
            messages.success(request, f"Your OTP is: {otp}") 

            user_email = request.POST.get('username')
            try:
                user = User.objects.get(username=user_email)
                send_mail(
                    "Your OTP Code",
                    f"Your OTP is: {otp}",
                    "DummyEmail7066@gmail.com", 
                    [user.email],
                    fail_silently=False,
                )
                messages.success(request, "OTP sent to your registered email.")
            except User.DoesNotExist:
                messages.error(request, "User not found. Please check your username.")

        elif "login" in request.POST and form.is_valid():
            user = form.get_user()
            otp = request.POST.get("otp")
            session_otp = request.session.get("otp")

            if session_otp and str(otp) == str(session_otp):
                login(request, user)
                return redirect("add") 
            else:
                messages.error(request, "Invalid OTP!")

    return render(request, "myapp/signin.html", {"form": form})
    
    
def send_results_email(request):
    calculations = Arithmatic.objects.all()

    for calc in calculations:
        if calc.USER and calc.USER.email:  
            subject = "Your Calculation Result"
            message = f"""
            Hello {calc.USER.username},
            The result of {calc.a} {calc.operation_type} {calc.b} is {calc.operation}.
            Thank you for using our service.
            Best Regards,
            Madle Roshan
            """
            email = EmailMessage(
                subject,
                message,
                "DummyEmail7066@gmail.com",
                [calc.USER.email],
            )
            email.send(fail_silently=False)
        messages.success(request, "Emails sent successfully to all users.")
    return redirect("add")  # Redirect to the desired page
    

def signout(request):
    logout(request)
    return redirect('signin')
    

@login_required(login_url='/signin/')  
def addition(request):
    result = None

    if request.method == 'POST':
        a = int(request.POST.get('a', 0))
        b = int(request.POST.get('b', 0))
        operation = request.POST.get('operation')

        result = handle_calculation(a,b,operation,request.user)
        print(request.user.email)

        send_mail(
            'Calculation Result', 
            f'The result of {a} {operation} {b} is {result}',
            'DummyEmail7066@gmail.com',
            [request.user.email],
            fail_silently=False
        )

    return render(request, 'myapp/index.html', {'result': result})