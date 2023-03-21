from django.shortcuts import render

# Create your views here.

from .models import Product

def dashboard(request):
    """
    This view will render the dashboard page
    """
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'core/dashboard.html',context)