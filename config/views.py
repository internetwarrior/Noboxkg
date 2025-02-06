from django.shortcuts import render,redirect
import hashlib
import hmac
import time
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.models import User

def react_app(request):
    return render(request, 'index.html')




def redirect_to_home(request):
    return redirect('/')

