import asyncio
import aiohttp
import re
import requests



from django.forms import ModelForm, Form, ModelChoiceField, ChoiceField, CharField, HiddenInput
from carpark.models import Car, Trip, Point
from django.contrib.auth.models import User, Group
from authorization.models import Grade
from manager.price_counter import PriceCounter
from taxi.settings import GOOGLE_API_KEY




async def count_price(obj):
    print("counting started")
    async with aiohttp.ClientSession() as session:
        async with session.get("https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&mode=driving&key=%s" 
                % (obj.startpoint_coordinate.lat,
                   obj.startpoint_coordinate.lng,
                   obj.endpoint_coordinate.lat,
                   obj.endpoint_coordinate.lng,
                      GOOGLE_API_KEY)) as resp:
            print("https://maps.googleapis.com/maps/api/directions/json?origin=%s,%s&destination=%s,%s&mode=driving&key=%s" 
                % (obj.startpoint_coordinate.lat,
                   obj.startpoint_coordinate.lng,
                   obj.endpoint_coordinate.lat,
                   obj.endpoint_coordinate.lng,
                      GOOGLE_API_KEY))
            
            # 
            j = await resp.json()
            p1 = j["routes"][0]["legs"][0]["distance"]["value"]
            print(p1)
            
            counter = PriceCounter()
            obj.price = counter.count_price(p1/1000)
            obj.save()

    
    print("DOne!")


async def save_all_trip(obj, client):
    obj.client = client
    obj.save()


class CarForm(ModelForm):
    class Meta:
        model = Car
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        self.fields['driver'].queryset = User.objects.filter(groups__name="Driver")


class AddDriverForm(Form):
    user = ModelChoiceField(queryset=User.objects.filter(groups__name="Client"))

    def save(self):
        u = self.cleaned_data['user']
        Group.objects.get(name="Client").user_set.remove(u)
        Group.objects.get(name="Driver").user_set.add(u)


class AddTripForm(Form):

    # class Meta:
    #     model = Trip
    #     fields = ['startpoint', 'startpoint_coordinate', 'endpoint', 'endpoint_coordinate']
    startpoint = CharField(widget=HiddenInput())
    endpoint = CharField(widget=HiddenInput())
    start_lat = CharField(widget=HiddenInput())
    start_lng = CharField(widget=HiddenInput())
    end_lat = CharField(widget=HiddenInput())
    end_lng = CharField(widget=HiddenInput())

    def save(self, client, *args, **kwargs):
        # obj = super(AddTripForm, self).save(commit=False, *args, **kwargs)
        print("ok")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        print("?")
        obj = Trip(startpoint=self.cleaned_data['startpoint'], endpoint=self.cleaned_data['endpoint'])
        
        print("exe")

        obj.startpoint_coordinate =  Point.objects.create(lat=self.cleaned_data['start_lat'], 
                                                          lng=self.cleaned_data['start_lng'])
        obj.endpoint_coordinate =  Point.objects.create(lat=self.cleaned_data['end_lat'], 
                                                          lng=self.cleaned_data['end_lng'])
        loop.run_until_complete(asyncio.wait([count_price(obj), save_all_trip(obj, client)]))
        loop.close()
        
        print("to user")


        
        


        



class RateDriver(Form):

    driver = HiddenInput()
    value = ChoiceField(choices=[(x, x) for x in range(6)])

    def save(self, client, *args, **kwargs):
        try:
            driver = User.objects.get(self.cleaned_data['driver'])
            grade = Grade.objects.filter(driver=driver, client=client)
            if grade:
                grade.value = value
                grade.save()
            elif driver.groups.filter(name="Driver").exists():
                g = Grade.objects.create(driver=driver, client=client, value=value)
        except:
            pass    
