from django.shortcuts import render
from django.contrib.auth import login, logout
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
                # Post Login Code
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
                # Post Login Code

    return render(request, 'signup.html', context)