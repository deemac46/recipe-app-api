from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'




# def homePageView(request):

#     return HttpResponse('Hello World')
    
class AboutPageView(TemplateView):
    template_name = 'about.html'