from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse

# Create your views here.
from .forms import VendorForm
from users.decorators import vendor_user
from users.models import CustomUser as User
from core.models import Product, Order
from .models import Vendor

@vendor_user
def vendor_form(request):
    form = VendorForm()

    if request.method == 'POST':
        form = VendorForm(request.POST)
        user = User.objects.get(id=request.user.id)

        if form.is_valid():
            vendor_data = form.save(commit=False)
            vendor_data.user = request.user
            vendor_data.save()
            user.is_vendor = True
            user.save()
            messages.success(request, 'You can now start selling')
            return redirect('dashboard')

    context = {
        'form': form
    }
    return render(request, 'vendor/vendor-form.html',context)


def vendor_dashboard(request):

    vendor = Vendor.objects.get(user=request.user)
    count =  Product.objects.filter(vendor=vendor).count()
    order_count = Order.objects.filter(vendor=vendor).count()


    if request.method == 'POST':
        search = request.POST['search']
        products = Product.objects.filter(name__icontains=search,vendor=vendor).order_by('-created_at')
    else:
        products = Product.objects.filter(vendor=vendor).order_by('-created_at')

    page = Paginator(products, 10)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)


    context = {
        'page': page,
        'count': count,
        'order_count': order_count
    }

    return render(request, 'vendor/vendor-dashboard.html',context)