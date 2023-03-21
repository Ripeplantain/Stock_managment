from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
from .models import Product

@login_required(login_url='login')
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

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    """
    This view will render the admin page
    """

    count =  Product.objects.count()

    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'count': count,
    }

    return render(request, 'core/admin.html',context)


@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, id):
    """
    This view will delete a product from the database
    """
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin')