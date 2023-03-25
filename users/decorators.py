from django.shortcuts import redirect

def authenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def vendor_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_vendor:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_func


def vendor_allowed(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_vendor:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('dashboard')
    return wrapper_func