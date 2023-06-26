from django.shortcuts import render
from harvester.models import Video, Query

def home(request):
    return render(request, 'home.html')

def api_key(request):
    return render(request, 'api_key.html')

def queries(request):
    queries = Query.objects.all()
    return render(request, 'queries.html', {'queries': queries})
