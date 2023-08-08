from django.core.cache import cache
from .models import SystemState

def get_system_state():
    state = cache.get('system_state')
    if state is None:
        state, _ = SystemState.objects.get_or_create(pk=1, defaults={"is_running": False})
        cache.set('system_state', state)
    return state

def set_system_state(is_running):
    state, _ = SystemState.objects.get_or_create(pk=1, defaults={"is_running": False})
    state.is_running = is_running
    state.save()
    cache.set('system_state', state)
