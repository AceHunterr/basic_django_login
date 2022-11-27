from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect



def send_email(request):
    subject = 'Subject'
    message = 'This is a test email'
    from_email = 'aggarwalmehul26@gmail.com'
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ['aggarwalmehul26@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/contact/thanks/')
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse('Make sure all fields are entered and valid.')



def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"Account was created for: "+ user)

                return redirect('login')

        context = {"form":form}
        return render(request, 'login/register.html', context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('home')
            else:
                messages.info(request,"USERNAME or PASSWORD is incorrect")


        context = {}
        return render(request, 'login/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')


@login_required(login_url="login")
def homePage(request):
    # send_email(request)
    context = {}
    return render(request,"login/home.html", context)