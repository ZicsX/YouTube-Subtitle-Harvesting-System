import json
import logging
from django.shortcuts import render
from django.http import HttpResponse
from youtubeapi.models import APIKey
from harvester.tasks import search_and_download
from django.views.decorators.csrf import csrf_exempt
from .utils.cache_utils import get_system_state, set_system_state
from django.core.cache import cache
from web_interface.celery import app


logger = logging.getLogger(__name__)


def home(request):
    # Display the home page
    return render(request, "harvester/home.html")


def start_process(request):
    set_system_state(True)
    logger.info("Harvesting process started")
    search_and_download.delay()
    return HttpResponse("Process started")


def stop_process(request):
    set_system_state(False)
    logger.info("Harvesting process stopped")
    # Fetch the task id and revoke it
    task_id = cache.get('search_and_download_task_id')
    if task_id:
        app.control.revoke(task_id)
        cache.delete('search_and_download_task_id')  # Optional: clear the task id from cache
    return HttpResponse("Process stopped")


@csrf_exempt
def update_api_key(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_api_key = data.get("api_key", "")
        if new_api_key:
            api_key, created = APIKey.objects.get_or_create(
                pk=1, defaults={"key": new_api_key}
            )
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
    state = get_system_state()
    api_key, _ = APIKey.objects.get_or_create(pk=1, defaults={"key": ""})
    logger.info(
        f"System is {'running' if state.is_running else 'stopped'}. Current API key is {api_key.key}"
    )
    return HttpResponse(
        f"System is {'running' if state.is_running else 'stopped'}. Current API key is {api_key.key}"
    )
