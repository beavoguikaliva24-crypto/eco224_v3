import threading

_thread_locals = threading.local()

def get_current_user():
    """
    Renvoie l'utilisateur actuellement connecté, s'il existe.
    """
    return getattr(_thread_locals, 'user', None)

class CurrentUserMiddleware:
    """
    Middleware qui stocke l'utilisateur de la requête actuelle dans une variable
    globale de thread.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Stocke l'utilisateur (même s'il est anonyme)
        _thread_locals.user = getattr(request, 'user', None)
        response = self.get_response(request)
        # Nettoie la variable après la requête
        del _thread_locals.user
        return response