from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employees
from datetime import date
from django.urls import reverse
import datetime


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.


def index(request):
    # This line will get the Customer model from the other app, it can now be used to query the db
    Customer = apps.get_model('customers.Customer')
    user = request.user
    this_employee = Employees.objects.get(user_id=user.id)
    return render(request, 'employees/index.html')


def create(request):
    if request.method == 'POST':
        user = request.user
        name = request.POST.get('name')
        zip_code = request.POST.get('zip_code')
        new_employee = Employees(name=name, zip_code=zip_code, user=user)
        new_employee.save()
        return HttpResponseRedirect(reverse('employees:index'))
    else:
        return render(request, 'employees/create.html')


def confirm_pickup(request, customer_id):
    Customer = apps.get_model('customers.Customer')
    customer = Customer.objects.get(pk=customer_id)
    customer.account_balance += 5
    customer.save()
    context = {
        'customer': customer
    }
    return render(request, 'employees/confirm.html', context)


def customer_in_zip(request):
    user = request.user
    employee = Employees.objects.get(user_id=user.id)
    Customer = apps.get_model('customers.Customer')
    customers = Customer.objects.all()
    same_zip = []
    for customer in customers:
        if customer.zipcode == employee.zip_code:
            same_zip.append(customer)
            context = {
                'customers': same_zip
            }
    return render(request, 'employees/customer_in_zip.html', context)


def define_day(request):
    if request.method == 'POST':
        user = request.user
        employee = Employees.objects.get(user_id=user.id)
        employee.define_day = request.POST.get('define_day')
        employee.save()
        return HttpResponseRedirect(reverse('employees:index'))

    return render(request, 'employees/index.html')


