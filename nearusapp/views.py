from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect

from script import get_places,unpack_places,unpack_target_places,Place,centroid,haversine_distance,distance_based_decision

# Create your views here.

from .forms import UserLocation

#masih buat development saja
def get_location(request):
    if request.method=="POST":
        form=UserLocation(request.POST)
        if form.is_valid():
            print("im in")
            address_1=form.cleaned_data['user_place_1']
            address_2=form.cleaned_data['user_place_2']
            address_3=form.cleaned_data['user_place_3']
            address_4=form.cleaned_data['target_place']
            user_addresses=[address_1,address_2,address_3]
            user_places=[Place(unpack_places(get_places(ad_users))) for ad_users in user_addresses]
            target_places=[Place(ad_target) for ad_target in unpack_target_places(get_places(address_4))]
            print(user_places)
            print(target_places)
            result=distance_based_decision(5,target_places,user_places)
            ready=True
            return render(request,'cobacobaform.html',{'result':result,'ready':ready})
    else:
        form=UserLocation()
    return render(request,'cobacobaform.html',{'form':form})