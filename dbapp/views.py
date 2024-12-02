from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView 
from django.db import connection 
from django.urls import reverse_lazy
from .models import Vehicles, Reservations
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Vehicles, Reservations, Users
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages




def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def add_vehicle(request):
    if request.method == 'POST':
        # Get form data
        vehicle = Vehicles.objects.create(
            ownerid_id=request.POST['owner_id'],
            make=request.POST['make'],
            model=request.POST['model'],
            year=request.POST['year'],
            dailyrate=request.POST['dailyrate'],
            location=request.POST['location'],
            isavailable=True
        )
        return redirect('list_page')
    return render(request, 'dbapp/add_vehicle.html')

@user_passes_test(is_admin)
def delete_vehicle(request, vehicle_id):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)
        vehicle.delete()
    return redirect('list_page')

def list_page(request):
    vehicles = Vehicles.objects.filter(isavailable=True)
    return render(request, 'dbapp/list_page.html', {'vehicles': vehicles})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            # Add error message handling here
            return render(request, 'dbapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'dbapp/login.html')


def logout_view(request):
    logout(request)
    return redirect('homepage')


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
        
        if password != password2:
            return render(request, 'dbapp/register.html', {'error': 'Passwords do not match'})
            
        # Create user in your Users table
        user = Users.objects.create(
            username=username,
            email=email,
            passwordhash=password,  # In production, you should hash this password
            usertype='Renter',
            dateregistered=timezone.now()
        )
        
        return redirect('login')
    return render(request, 'dbapp/register.html')



def homepage(request):
    return render(request, 'dbapp/homepage.html')

def test_view(request):
    return render(request, 'vehicle_list.html')




def vehicle_list(request):
    vehicles = Vehicles.objects.filter(isavailable=True).order_by('-year')
    paginator = Paginator(vehicles, 9)  # Show 9 vehicles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'dbapp/vehicle_list.html', {'vehicles': page_obj})

def testmysql(request):
    """
    A simple view to verify database connection and test the application.
    """
    return render(request, 'dbapp/testmysql.html', {'message': 'Hello, Django!'})


# Vehicle Reservation View
def reserve_vehicle(request, vehicle_id):
    """
    Placeholder View for reserving a vehicle.
    This will allow users to reserve a specific vehicle once migrations are complete.
    """
    vehicle = get_object_or_404(Vehicles, vehicleid=vehicle_id)
    # Fetch existing reservations for this vehicle
    reservations = Reservations.objects.filter(vehicleid=vehicle).order_by('startdate')

    if request.method == 'POST':
        renter_id = request.POST['renter_id']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Check for overlapping reservations
        overlapping_reservations = reservations.filter(
            Q(startdate__lte=end_date, enddate__gte=start_date)
        )
        if overlapping_reservations.exists():
            return render(request, 'reserve_vehicle.html', {
                'vehicle': vehicle,
                'reservations': reservations,
                'error': 'This vehicle is not available for the selected dates.'
            })

        # Create the reservation
        renter = get_object_or_404(Renter, id=renter_id)
        Reservations.objects.create(
            vehicleid=vehicle,
            renterid=renter,
            startdate=start_date,
            enddate=end_date,
            reservationstatus='Pending'  # Example default status
        )
        return redirect('vehicle_list') 

    return render(request, 'dbapp/reserve_vehicle.html', {'vehicle': vehicle})



# Optional Reservation List View
def reservation_list(request, renter_id):
    """
    Placeholder View for listing all reservations for a specific renter.
    """
    reservations = Reservations.objects.filter(renterid_id=renter_id)
    return render(request, 'reservation_list.html', {'reservations': reservations})

# Listing car for rent
def list_car(request):
    if request.method == 'POST':
        make = request.POST['make']
        model = request.POST['model']
        year = request.POST['year']
        price = request.POST['price']
        location = request.POST['location']
        
        # Save the car information
        Vehicles.objects.create(
            make=make,
            model=model,
            year=year,
            dailyrate=price,
            location=location,
            isavailable=1  # Set car availability to true
        )
        return redirect('listing_rental_car')  # Redirect to the vehicle list page after listing
    
    return render(request, 'dbapp/listing_rental_car.html')
  # Use the correct file name

