from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from users.forms import CreateUserForm


# Create your views here.
from .models import Product, Order
from .forms import ProductForm, CreateOrder

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

@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    """
    This view will render the admin page
    """

    count =  Product.objects.count()
    users_count = User.objects.exclude(is_superuser=True).count()
    order_count = Order.objects.count()


    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search).order_by('-created_at')
    else:
        products = Product.objects.all().order_by('-created_at')

    page = Paginator(products, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)


    context = {
        'page': page,
        'count': count,
        'users_count': users_count,
        'order_count': order_count
    }

    return render(request, 'core/product.html',context)


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
    

@user_passes_test(lambda u: u.is_superuser)
def view_users(request):
    """
    This view will render the users page
    """
    count =  Product.objects.count()
    users_count = User.objects.exclude(is_superuser=True).count()
    order_count = Order.objects.count()


    search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST['search']
        users = User.objects.filter(Q(username__icontains=search)|
                                          Q(first_name__icontains=search)|Q(last_name__icontains=search)|
                                          Q(email__icontains=search)).order_by('-date_joined')
    else:
        users = User.objects.all().order_by('-date_joined').exclude(is_superuser=True)


    page = Paginator(users, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)


    context = {
        'page': page,
        'count': count,
        'users_count': users_count,
        'order_count': order_count
    }

    return render(request, 'core/users.html',context)


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
            product_order = form.save(commit=False)
            product_order.user = request.user
            product_order.product = product
            product_order.save()
            messages.success(request, 'Order created successfully')
            return redirect('dashboard')
    

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
    form = CreateUserForm(instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'core/profile.html',context)


@user_passes_test(lambda u: u.is_superuser)
def order_history(request):
    """
        This is for the order history
    """

    count =  Product.objects.count()
    users_count = User.objects.exclude(is_superuser=True).count()
    order_count = Order.objects.count()

    search = request.GET.get('search')

    if request.method == 'POST':
        search = request.POST['search']
        orders = Order.objects.filter(Q(product__icontains=search)|
                                          Q(user__icontains=search)|Q(number__icontains=search)|
                                          Q(address__icontains=search)).order_by('-created_at')
    else:
        orders = Order.objects.filter(processed=False).order_by('-created_at')


    page = Paginator(orders, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page': page,
        'count': count,
        'users_count': users_count,
        'order_count': order_count
    }
   
    return render(request, 'core/order_history.html',context)


@user_passes_test(lambda u: u.is_superuser)
def process_order(request,id):
    """
        This is for processing the order
    """

    order = get_object_or_404(Order, id=id)
    order.processed = True
    order.save()
    messages.success(request, 'Order processed successfully')

    return redirect('orders')


@user_passes_test(lambda u: u.is_superuser)
def update_order(request,id):
    """
        This is for updating the order
    """

    order = get_object_or_404(Order, id=id)
    form = CreateOrder(instance=order)

    if request.method == 'POST':
        form = CreateOrder(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order updated successfully')
            return redirect('orders')

    context = {
        'form': form
    }

    return render(request, 'core/update_order.html',context)