from django.shortcuts import redirect
from django.contrib.auth import logout

class RedirectAnd404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        path = request.path.lower()

        # ------------------------------
        # 1. Ignore SAFE requests
        # ------------------------------
        if (
            path.startswith('/static/') or
            path.startswith('/media/') or
            path.startswith('/favicon') or
            path.endswith('.css') or
            path.endswith('.js') or
            path.endswith('.png') or
            path.endswith('.jpg') or
            path.endswith('.jpeg') or
            path.endswith('.svg') or
            path.endswith('.gif') or
            path.startswith('/admin/')
        ):
            return response

        # ------------------------------
        # 2. Only logout on REAL 404 pages
        # ------------------------------
        if response.status_code == 404:

            if request.user.is_authenticated:
                logout(request)
                return redirect('login')

            return redirect('login')

        return response
