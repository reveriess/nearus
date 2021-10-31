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
    context = {
        "form": UserLocation(),
        "result": None,
        "staticimg_url": None,
    }

    staticimg_url = "https://maps.googleapis.com/maps/api/staticmap?"

    if request.method == "POST":
        form = context["form"] = UserLocation(request.POST)

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
            staticimg_url = staticmaps_func(
                staticimg_url, user_latlong, target_latlong, centroid_users
            )

            context["result"] = result_short
            context["staticimg_url"] = staticimg_url
            return render(request, "cobacobaform.html", context)
    else:
        form = UserLocation()

    return render(request, "cobacobaform.html", context)
