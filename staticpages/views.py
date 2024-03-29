from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.contrib import messages
from .forms import CategoryForm, ContactForm, UserProfileForm
from django.core.mail import send_mail

def index(request):
    context = {'title': 'home'}
    return render(request, 'staticpages/index.html', context)

def about(request):
    context = {'title' : 'about'}
    return render(request, 'staticpages/about.html', context)

from django.shortcuts import render
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            send_mail(
                'Contact Form Submission from {}'.format(name),
                message,
                email,
                ['warsamegift@gmail.com'],  # Replace with your email
            )
            return redirect('marketplace:contact_success')
        else:
            # Form is not valid, so render the form with errors
            return render(request, 'staticpages/contact.html', {'form': form})
    else:
        form = ContactForm()
    return render(request, 'staticpages/contact.html', {'form': form})

def contact_success(request):   
    return render(request, 'staticpages/contact_success.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'staticpages/contact_success.html', {'form':form})
    else:
        form = ContactForm()

    return render(request, 'staticpages/contact.html', {'form':form})

def help(request):
    context = {'title': 'help'}
    return render(request, 'staticpages/help.html', context)

def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    context = {'title': 'login', 'form': form}
    return render(request, 'staticpages/account/login.html', context)


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                return HttpResponse('A user with this email already exists.')
            user = form.save()  # Save the user instance
            # Log in the user after successful registration
            login(request, user)
            # Redirect to the home page after successful registration
            return redirect('home')
        else:
            return HttpResponse('Invalid Registration')
    else:
        form = SignUpForm()
    context = {'title': 'register', 'form': form}
    return render(request, 'staticpages/account/register.html', context)
            
def search(request):
    context = {'title': 'search'}
    return render(request, 'marketplace/search.html', context)

@login_required
def chat(request):
    context = {'title': 'chat'}
    return render(request, 'staticpages/chat.html', context)

@login_required
def orders(request):
    context = {'title': 'orders'}
    return render(request, 'orders/order.html', context)

def password_reset(request):
    context = {'title': 'password_reset'}
    return render(request, 'staticpages/registration/password_change_form.html', context)


@login_required
def user_profile(request):
    if request.method == 'POST':
        user_form = ProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('staticpages/account/profile')
    else:
        user_form = ProfileForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user)
        
    return render(request, 'staticpages/account/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def cart(request):
    context = {'title': 'cart'}
    return render(request, 'marketplace/cart.html', context)

@require_POST
def signout(request):
    logout(request)
    context = {'title': 'signout'}
    return render(request, 'staticpages/account/logout.html', context)

@login_required
def dashboard(request):
    context = {'title' : 'dashboard'}
    return render(request, 'staticpages/dashboard.html', context )

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:categories')
    else:
        form = CategoryForm()
    return render(request, 'staticpages/add_category.html', {'form': form})

