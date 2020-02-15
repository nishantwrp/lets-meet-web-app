from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView),
    path('signup/', signUpView),
    path('dashboard/', dashboardView),
    path('schedule/', scheduleView),
    path('meet/<int:pk>/', meetupView),
]
