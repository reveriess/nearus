from django.shortcuts import render
from script import (
    save_to_media,
    gmaps,
    Place,
    centroid,
    distance_based_decision,
)

from .forms import UserLocation

# masih buat development saja
def get_location(request):
    context = {
        "form": UserLocation(),
        "result": None,
        "staticimg_url": None,
    }

    if request.method == "POST":
        form = context["form"] = UserLocation(request.POST)

        if form.is_valid():
            print("im in")
            address_1 = form.cleaned_data["user_place_1"]
            address_2 = form.cleaned_data["user_place_2"]
            address_3 = form.cleaned_data["user_place_3"]
            address_4 = form.cleaned_data["target_place"]
            zoom_level = form.cleaned_data["zoom_level"]

            user_addresses = [address_1, address_2, address_3]
            user_places = [
                Place(gmaps.get_place(ad_users)) for ad_users in user_addresses
            ]
            user_latlong = [i.get_latlong() for i in user_places]

            centroid_latlong = centroid(user_places)
            target_places = [
                Place(ad_target)
                for ad_target in gmaps.get_places_target(address_4, centroid_latlong)
            ]

            result_short, result_place = distance_based_decision(
                5, target_places, user_places
            )

            target_latlong = [i.get_latlong() for i in result_place]
            static_map = gmaps.get_static_map(
                user_latlong, target_latlong, centroid_latlong, zoom_level
            )
            static_map_filename = save_to_media(static_map)

            context["result"] = result_short
            context["staticimg_url"] = f"/media/{static_map_filename}"
            return render(request, "cobacobaform.html", context)
    else:
        form = UserLocation()

    return render(request, "cobacobaform.html", context)
