from django.shortcuts import render
from .forms import APIKeyForm, SeedQueryForm

def api_key_update(request):
    if request.method == 'POST':
        form = APIKeyForm(request.POST)
        if form.is_valid():
            api_key = form.cleaned_data['api_key']
            # TODO: Save this key to your settings or database
    else:
        form = APIKeyForm()

    return render(request, 'api_key_form.html', {'form': form})

def seed_query_update(request):
    if request.method == 'POST':
        form = SeedQueryForm(request.POST)
        if form.is_valid():
            seed_query = form.cleaned_data['seed_query']
            # TODO: Save this query to your settings or database
    else:
        form = SeedQueryForm()

    return render(request, 'seed_query_form.html', {'form': form})
