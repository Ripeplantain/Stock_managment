from django.shortcuts import render

# Create your views here.

from .models import Product

def dashboard(request):
    """
    This view will render the dashboard page
    """
    
    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, 'core/dashboard.html',context)