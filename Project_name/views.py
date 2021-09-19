from django.shortcuts import render, redirect

#-------------------------------------------------------------------------------
#   Views for the base directory only deals with the index page aka home page
#   These are simple redirects. Everything else is taken care
#   of in the other apps.

def index(request):
    return render(request, 'Project_name/index.html')