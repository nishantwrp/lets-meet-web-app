from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
import requests

def send_api_request(url ,data = None, request = None):
    if request:
        headers = {
            'Authorization': 'Token ' + request.user.username
        }
        if data:
            return requests.post('https://lets-meet-backend.herokuapp.com/' + url, data=data, headers=headers)
        else:
            return requests.get('https://lets-meet-backend.herokuapp.com/' + url, headers=headers)
    else:
        if data:
            return requests.post('https://lets-meet-backend.herokuapp.com/' + url, data=data)
        else:
            return requests.get('https://lets-meet-backend.herokuapp.com/' + url)

# Permissions

def indexView(request):
    
    return render(request, 'index.html')

def signUpView(request):
    context = {}

    if request.method ==  'POST':
        # Signup
        if 'signup' in request.POST:
            data = {
                "email": request.POST['email'],
                "first_name": request.POST['first_name'],
                "last_name": request.POST['last_name'],
                "password": request.POST['password']
            }
            r = send_api_request('register/', data)
            if r.status_code == 200:
                token_json = r.json()
                user, created = User.objects.get_or_create(username=token_json['token'])
                if created:
                    user.first_name = request.POST['first_name']
                    user.last_name = request.POST['last_name']
                    user.save()
                login(request, user)
                return redirect(dashboardView)
        else:
            data = {
                "email": request.POST['login_email'],
                "password": request.POST['login_password']
            }
            r = send_api_request('login/', data)
            if r.status_code == 200:
                token_json = r.json()
                user, created = User.objects.get_or_create(username=token_json['token'])
                login(request, user)
                return redirect(dashboardView)

    return render(request, 'signup.html', context)

def dashboardView(request):
    context = {}

    def logout_user(request):
        if 'logout' in request.GET:
            if request.GET['logout'] == 'true':
                logout(request)
                return True
        return False

    context['name'] = request.user.first_name + ' ' + request.user.last_name

    r = send_api_request('meets/',request=request)

    meets = r.json()
    all_meets = list()
    for meet in meets['created_meets']:
        all_meets.append(meet)
    for meet in meets['participating_meets']:
        all_meets.append(meet)
    context['meets'] = all_meets
    return render(request, 'dashboard.html', context)

def scheduleView(request):
    context = {}


    def logout_user(request):
        if 'logout' in request.GET:
            if request.GET['logout'] == 'true':
                logout(request)
                return True
        return False

    context['name'] = request.user.first_name + ' ' + request.user.last_name
    if request.method == 'POST':
        context['toast'] = True

    return render(request, 'schedule.html', context)