from datetime import datetime


from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from carpark.forms import CarForm, AddDriverForm, AddTripForm
from django.http import HttpResponse
from django.views.generic import ListView, View
from django.views.generic.edit import FormView
from .models import Car, Trip

# Create your views here.

class CarFormView(LoginRequiredMixin, FormView):
    form_class = CarForm
    template_name = "carpark/car.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super(CarFormView, self).form_valid(form)


class AddDriverFormView(LoginRequiredMixin, FormView):
    form_class = AddDriverForm
    template_name = "carpark/driver.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        return super(AddDriverFormView, self).form_valid(form)


class AddTripFormView(LoginRequiredMixin, FormView):
    form_class = AddTripForm
    template_name = "carpark/trip.html"
    success_url = "/"

    def form_valid(self, form):
        form.save(client=self.request.user)
        return super(AddTripFormView, self).form_valid(form)


class NonAcceptedTripsView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = "carpark/trips.html"

    def dispatch(self, request):
        car = Car.objects.get(driver=request.user)
        if Trip.objects.filter(car=car, end_time=None).exists():
            return HttpResponse("You have a trip!")
        return super(NonAcceptedTripsView, self).dispatch(request)


    def get_queryset(self):
        return Trip.objects.filter(car=None)


class AcceptTripView(LoginRequiredMixin, View):

    def get(self, request, trip_id):
        try:
            car = Car.objects.get(driver=request.user)
            if Trip.objects.filter(car=car, end_time=None).exists():
                return HttpResponse("Trip is already exists")
            t = Trip.objects.get(id=trip_id)
            if t.car:
                return HttpResponse("sorry")
            else:
                t.car = Car.objects.get(driver=request.user)
                t.save()
                return HttpResponse("OK")
        except:
            return HttpResponse("Doesn't exist")


class NonClosedTripsView(LoginRequiredMixin, ListView):
    model = Trip
    template_name = "carpark/trips_opened.html"

    def dispatch(self, request):
        car = Car.objects.get(driver=request.user)
        self.queryset = Trip.objects.filter(car=car, end_time=None)
        return super(NonClosedTripsView, self).dispatch(request)




class CloseTripView(LoginRequiredMixin, View):

    def get(self, request, trip_id):
        try:
            t = Trip.objects.get(id=trip_id)
            car = Car.objects.get(driver=request.user)
            if t.car and t.car == car:
                t.end_time = datetime.now()
                t.save()
                return HttpResponse("OK")
            else:
                return HttpResponse("sorry")
        except:
            return HttpResponse("Doesn't exist")