
from django.utils.cache import add_never_cache_headers

class NoCacheMiddleware:
    """Middleware to prevent browser caching issues that cause stuck pages"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add headers to prevent caching for dynamic pages
        if request.path.startswith('/add/') or request.path.startswith('/delete/'):
            add_never_cache_headers(response)
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response