from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Customer
from django.urls import reverse
# Create your views here.

# TODO: Create a function for each path created in customers/urls.py. Each will need a template as well.


def index(request):
    # The following line will get the logged-in in user (if there is one) within any view function
    user = request.user
    # It will be necessary while creating a customer/employee to assign the logged-in user as the user foreign key
    # This will allow you to later query the database using the logged-in user,
    # thereby finding the customer/employee profile that matches with the logged-in user.
    try:
        logged_in_customer = Customer.objects.get(user=user)
        context = {
            'logged_in_customer': logged_in_customer
        }
    except:
        return HttpResponseRedirect(reverse('customers:sign_up'))

    return render(request, 'customers/index.html', context)


def sign_up(request):
    if request.method == "POST":
        name = request.POST.get('name')
        pickup_day = request.POST.get('pickup_day')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        new_account = Customer(user=request.user, name=name, pickup_day=pickup_day, address=address, zipcode=zipcode)
        new_account.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/sign_up.html')


def change(request):
    user = request.user
    specific_customer = Customer.objects.get(user_id=user.id)
    if request.method == 'POST':
        specific_customer.pickup_day = request.POST.get('pickup_day')
        specific_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/change.html')


def one_time_pickup(request):
    user = request.user
    specific_customer = Customer.objects.get(user_id=user.id)
    if request.method == 'POST':
        specific_customer.one_time_pickup = request.POST.get('one_time_pickup')
        specific_customer.save()
        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/one_time_pickup.html')


def suspend_account(request):
    if request.method == 'POST':
        user = request.user
        customer = Customer.objects.get(user_id=user.id)
        customer.suspension_start = request.POST.get('suspension_start')
        customer.suspension_end = request.POST.get('suspension_end')
        customer.save()

        return HttpResponseRedirect(reverse('customers:index'))
    else:
        return render(request, 'customers/suspend_account.html')
