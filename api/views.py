from django.shortcuts import render

# Create your views here.
# myapp/views.py
from django.http import JsonResponse
data =[]



def tuk_tuk_view(request):
    return JsonResponse(data, safe=False)
