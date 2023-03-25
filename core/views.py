from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404
from users.forms import UpdateUserForm


# Create your views here.
from .models import Product, Order
from vendor.models import Vendor    
from users.models import CustomUser as User
from .forms import ProductForm, CreateOrder, UpdateOrder
from users.decorators import vendor_allowed


@login_required(login_url='login')
def dashboard(request):
    """
    This view will render the dashboard page
    """
    
    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')

    page = Paginator(products, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page
    }
    return render(request, 'core/dashboard.html',context)


@vendor_allowed
def delete_product(request, id):
    """
    This view will delete a product from the database
    """
    product = Product.objects.get(id=id)
    product.delete()
    messages.success(request, 'Product deleted successfully')
    return redirect('vendor-dashboard')


@vendor_allowed
def create_product(request):
    """
    This view will create a product in the database
    """
    form = ProductForm()
    vendor = Vendor.objects.get(user=request.user)

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product_data = form.save(commit=False)
            product_data.vendor = vendor
            product_data.save()
            messages.success(request, 'Product created successfully')
            return redirect('vendor-dashboard')
    else:
        return render(request, 'core/create_product.html', {'form': form})


@vendor_allowed
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
            return redirect('vendor-dashboard')
    else:
        return render(request, 'core/update_product.html', {'form': form})
    

@login_required(login_url='login')
def order_view(request,id):
    """
        This is for the order view
    """

    product = get_object_or_404(Product, id=id)
    form = CreateOrder()

    if request.method == 'POST':
        form = CreateOrder(request.POST)
        if form.is_valid():
            if product.quantity >= form.cleaned_data['quantity']:
                product.quantity -= form.cleaned_data['quantity']
                product.save()
                product_order = form.save(commit=False)
                product_order.user = request.user
                product_order.product = product
                product_order.vendor = product.vendor
                product_order.save()
                messages.success(request, 'Order created successfully')
                return redirect('dashboard')
            else:
                messages.error(request, 'Order quantity is greater than available quantity')
                return redirect('order-product', id=id)

    context = {
        'product': product,
        'form': form
    }

    return render(request, 'core/order.html',context)


@login_required(login_url='login')
def profile_page(request):
    """
        This is for the profile page
    """
    form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'core/profile.html',context)


@vendor_allowed
def order_history(request):
    """
        This is for the order history
    """

    vendor = Vendor.objects.get(user=request.user)

    count =  Product.objects.filter(vendor=vendor).count()
    order_count = Order.objects.filter(processed=False).count()


    search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST['search']
        orders = Order.objects.filter(Q(product__icontains=search)|
                                          Q(user__icontains=search)|Q(number__icontains=search)|
                                          Q(address__icontains=search) & Q(vendor=vendor)).order_by('-created_at')
    else:
        orders = Order.objects.filter(processed=False,vendor=vendor).order_by('-created_at')


    page = Paginator(orders, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page,
        'count': count,
        'order_count': order_count
    }
   
    return render(request, 'core/order_history.html',context)


@vendor_allowed
def process_order(request,id):
    """
        This is for processing the order
    """

    order = get_object_or_404(Order, id=id)
    order.processed = True
    order.save()
    messages.success(request, 'Order processed successfully')

    return redirect('orders')


@vendor_allowed
def update_order(request,id):
    """
        This is for updating the order
    """

    order = get_object_or_404(Order, id=id)
    form = UpdateOrder(instance=order)

    if request.method == 'POST':
        form = UpdateOrder(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully')
            return redirect('orders')

    context = {
        'form': form
    }

    return render(request, 'core/update_order.html',context)


@vendor_allowed
def delete_order(request,id):
    """
        This is for deleting the order
    """

    order = get_object_or_404(Order, id=id)
    product = get_object_or_404(Product, id=order.product.id)
    product.quantity += order.quantity
    product.save()
    order.delete()
    messages.success(request, 'Order deleted successfully')

    return redirect('orders')