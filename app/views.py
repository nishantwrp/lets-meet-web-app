from django.shortcuts import render

# Create your views here.

def indexView(request):
    return render(request, 'index.html')

def signUpView(request):
    return render(request, 'signup.html')