from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.http import HttpResponse

# Create your views here.
from .models import Product
from .forms import ProductForm

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

@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    """
    This view will render the admin page
    """

    count =  Product.objects.count()

    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')

    context = {
        'products': products,
        'count': count,
    }

    return render(request, 'core/admin.html',context)


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, id):
    """
    This view will delete a product from the database
    """
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('admin')


@user_passes_test(lambda u: u.is_superuser)
def create_product(request):
    """
    This view will create a product in the database
    """
    form = ProductForm()
     
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully')
            return redirect('admin')
    else:
        return render(request, 'core/create_product.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser)
def update_product(request, id):
    """
    This view will update a product in the database
    """
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
     
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully')
            return redirect('admin')
    else:
        return render(request, 'core/update_product.html', {'form': form})