from django.shortcuts import render
from django.http import HttpResponse
from harvester.models import SystemState
from youtubeapi.models import APIKey
from harvester.tasks import search_and_download
from django.views.decorators.csrf import csrf_exempt
import json
import logging

logger = logging.getLogger(__name__)

def home(request):
    # Display the home page
    return render(request, 'harvester/home.html')

def start_process(request):
    state, created = SystemState.objects.get_or_create(pk=1, defaults={'is_running': True})
    if not created:
        state.is_running = True
        state.save()
    logger.info("Harvesting process started")

    # Dispatch the celery task
    search_and_download.delay()

    return HttpResponse("Process started")

def stop_process(request):
    state, created = SystemState.objects.get_or_create(pk=1, defaults={'is_running': False})
    if not created:
        state.is_running = False
        state.save()
    logger.info("Harvesting process stopped")

    return HttpResponse("Process stopped")

@csrf_exempt
def update_api_key(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_api_key = data.get('api_key', '')
        if new_api_key:
            api_key, created = APIKey.objects.get_or_create(pk=1, defaults={'key': new_api_key})
            if not created:
                api_key.key = new_api_key
                api_key.save()
            logger.info("API Key updated")
            return HttpResponse("API Key Updated")
        else:
            logger.warning("No API Key provided")
            return HttpResponse("No API Key Provided", status=400)
    else:
        logger.warning("Invalid request received for API Key update")
        return HttpResponse("Invalid Request", status=400)

def system_status(request):
    state, created = SystemState.objects.get_or_create(pk=1, defaults={'is_running': False})
    api_key, _ = APIKey.objects.get_or_create(pk=1, defaults={'key': ''})
    if not created:
        logger.info(f"System is {'running' if state.is_running else 'stopped'}. Current API key is {api_key.key}")
        return HttpResponse(f"System is {'running' if state.is_running else 'stopped'}. Current API key is {api_key.key}")
    else:
        logger.info("System is stopped. No API key set.")
        return HttpResponse("System is stopped. No API key set.")

def queries(request):
    return
