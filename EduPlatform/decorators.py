from django.shortcuts import redirect
from django.http import HttpResponse


def unauthenticated_user(view_func):
    '''
    Decorator for views that redirects authenticated users to home if they try
    to access views that are meant for unauthenticated users only

    Example: 
        user shouldn't have access to login, or register once they are logged in
    '''
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def redirecter_based_on_group(allowed_roles=[]):
    """
    Decorator for views that restricts access based on user group membership
    """
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            
            if request.user.groups.exists():
                user_groups = [group.name for group in request.user.groups.all()]

                for role in allowed_roles:
                    if role in user_groups:
                        return view_func(request, *args, **kwargs)
                    
            return HttpResponse("No está autorizado a ver esta página ¯\_(ツ)_/¯")
        return wrapper_func
    return decorator 
