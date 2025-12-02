
# accounts/middleware.py
from django.shortcuts import redirect
from django.contrib.auth import logout

class RedirectAnd404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if it's a 404 error
        if response.status_code == 404:
            # Logout the user if they're authenticated
            if request.user.is_authenticated:
                logout(request)
            
            # Redirect to home page (change 'base' to your actual home URL name)
            return redirect('home2')
        
        return response