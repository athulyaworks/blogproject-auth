from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from django.http import HttpResponseForbidden

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'blog/login.html', {'error': 'Invalid credentials'})

    return render(request, 'blog/login.html')


@login_required
def home(request):
    return render(request, 'blog/home.html')


@login_required
def dashboard(request):
   
    request.session['theme'] = request.session.get('theme', 'light')
    
    show_popup = request.COOKIES.get('welcome_shown') != 'yes'
    response = render(request, 'blog/dashboard.html', {
        'show_popup': show_popup,
        'theme': request.session['theme']
    })
    if show_popup:
        # Set cookie to expire in 7 days
        response.set_cookie('welcome_shown', 'yes', max_age=7*24*60*60)
    return response

@login_required
def admin_dashboard(request):
    print("Logged in user:", request.user.username)
    print("User groups:", list(request.user.groups.values_list('name', flat=True)))

    if request.user.groups.filter(name='Admins').exists():
        return render(request, 'blog/admin_dashboard.html')

    return render(request, '403.html', status=403)


def logout_view(request):
    logout(request)
    return redirect('login')
