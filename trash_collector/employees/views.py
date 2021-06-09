from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.apps import apps
from .models import Employees
from datetime import date
from django.urls import reverse
from django.db.models import Q


# Create your views here.

# TODO: Create a function for each path created in employees/urls.py. Each will need a template as well.

def index(request):
    user = request.user
    try:
        logged_in_employee = Employees.objects.get(user=user)
        context = {
            'logged_in_employee': logged_in_employee
        }
    except:
        return HttpResponseRedirect(reverse('employees:create'))
    employee = Employees.objects.get(user_id=user.id)
    Customer = apps.get_model('customers.Customer')
    customers = Customer.objects.all()
    customers_today = []
    today = date.today()
    for customer in customers:
        if customer.zipcode == employee.zip_code and customer.suspension == False and\
                customer.pickup_day == today.strftime('%A') or customer.one_time_pickup == today:
            customers_today.append(customer)
            context = {
                'customers': customers_today
            }
    return render(request, 'employees/index.html', context)



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


def filter_pickups(request):
    customers = apps.get_model('customers.Customer')
    employee = Employees.objects.get(user=request.user)
    employee_customers = customers.objects.filter(zipcode=employee.zip_code)
    if request.method == 'POST':
        filtered_customers = customers.objects.filter(zipcode=employee.zip_code).filter(pickup_day=request.POST.get('pickup_day'))
        context = {
            'customers': filtered_customers,
            'employee': employee
        }
        return render(request, 'employees/filter_pickups.html', context)
    else:
        context = {
            'customers': employee_customers
        }
        return render(request, 'employees/filter_pickups.html', context)