from django.shortcuts import redirect
from django.contrib.auth import logout
import logging
import traceback
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

# ============================================
# Diagnostic Middleware (for debugging)
# ============================================
class LogoutDetectionMiddleware(MiddlewareMixin):
    """
    Middleware to detect and log when logout() is called
    """
    
    def process_request(self, request):
        # Store original user
        request._original_user = request.user.is_authenticated
        request._original_username = request.user.username if request.user.is_authenticated else None
        return None
    
    def process_response(self, request, response):
        # Check if user was logged out during this request
        if hasattr(request, '_original_user') and request._original_user:
            if not request.user.is_authenticated:
                # User was logged out!
                logger.error(f"""
==================== LOGOUT DETECTED ====================
User '{request._original_username}' was logged out!
Path: {request.path}
Method: {request.method}
Status Code: {response.status_code}
Redirect Location: {response.get('Location', 'N/A')}

Stack trace:
{''.join(traceback.format_stack())}
=========================================================
                """)
                print(f"🔴 LOGOUT DETECTED: {request._original_username} on {request.path}")
        
        return response


# ============================================
# 404 Redirect Middleware (FIXED - NO LOGOUT!)
# ============================================
class RedirectAnd404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path.lower()

        # Ignore static/media files
        if (
            path.startswith('/static/') or
            path.startswith('/media/') or
            path.startswith('/favicon') or
            path.startswith('/__debug__') or
            '.' in path.split('/')[-1] or  # Any file with extension
            path.startswith('/admin/')
        ):
            return response

        # Handle 404 errors WITHOUT logging out
        if response.status_code == 404:
            if request.user.is_authenticated:
                return redirect('home2')  # Logged-in users go to home
            else:
                return redirect('login')  # Anonymous users go to login

        return response