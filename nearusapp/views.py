from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from staticmaps import staticmaps_func
from script import (
    get_places,
    unpack_places,
    unpack_target_places,
    Place,
    centroid,
    haversine_distance,
    distance_based_decision,
    get_places_target,
)

# Create your views here.

from .forms import UserLocation

# masih buat development saja
def get_location(request):
    staticimg_url = "https://maps.googleapis.com/maps/api/staticmap?"
    if request.method == "POST":
        form = UserLocation(request.POST)
        if form.is_valid():
            print("im in")
            address_1 = form.cleaned_data["user_place_1"]
            address_2 = form.cleaned_data["user_place_2"]
            address_3 = form.cleaned_data["user_place_3"]
            address_4 = form.cleaned_data["target_place"]
            user_addresses = [address_1, address_2, address_3]
            user_places = [
                Place(unpack_places(get_places(ad_users)))
                for ad_users in user_addresses
            ]
            user_latlong = [i.get_latlong() for i in user_places]
            centroid_users = centroid(user_places)
            target_places = [
                Place(ad_target)
                for ad_target in unpack_target_places(
                    get_places_target(address_4, centroid_users)
                )
            ]
            centroid_users, result_short, result_place = distance_based_decision(
                5, target_places, user_places
            )
            target_latlong = [i.get_latlong() for i in result_place]
            print(target_latlong)
            ready = True
            staticimg_url = staticmaps_func(
                staticimg_url, user_latlong, target_latlong, centroid_users
            )
            return render(
                request,
                "cobacobaform.html",
                {
                    "result": result_short,
                    "ready": ready,
                    "user_place_1_returned": address_1,
                    "user_place_2_returned": address_2,
                    "user_place_3_returned": address_3,
                    "target_place_returned": address_4,
                    "staticimg_url": staticimg_url,
                },
            )
    else:
        form = UserLocation()
    return render(request, "cobacobaform.html", {"form": form})
