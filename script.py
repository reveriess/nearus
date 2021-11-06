from datetime import datetime
from googlemaps.maps import StaticMapMarker
import googlemaps
import haversine as hs
from haversine import Unit

import os


class NearusException(Exception):
    pass


class GMaps:
    def __init__(self, api_key=None):
        if not api_key:
            api_key = os.environ.get("API_KEY")
        self.gmaps = googlemaps.Client(key=api_key)

    def _places(self, query=None, location=None):
        places = self.gmaps.places(query=query, location=location)
        status = places["status"]
        if status != "OK":
            raise NearusException(f"Google Places API returned status {status}")

        results = places["results"]
        return results

    # get user's location & generate the "place"
    def get_place(self, query):
        # results = list of dicts. disini ambil yang pertama dulu
        results = self._places(query)
        return results[0]  # places=dict

    def get_places_target(self, query, centroid):
        results = self._places(query, centroid)
        return results[:10]  # places=List[dict]

    def get_static_map(self, user_latlongs, target_latlongs, centroid_latlong):
        user_markers = StaticMapMarker(color="blue", label="U", locations=user_latlongs)
        target_markers = StaticMapMarker(
            color="red", label="T", locations=target_latlongs
        )
        centroid_marker = StaticMapMarker(
            color="yellow", label="C", locations=[centroid_latlong]
        )
        markers = [user_markers, target_markers, centroid_marker]

        return self.gmaps.static_map(
            size=(500, 500),
            scale=1,
            zoom=12,
            maptype="roadmap",
            style={"feature": "poi", "visibility": "off"},
            center=centroid_latlong,
            markers=markers,
        )


gmaps = GMaps()

# places hasil search jadi object. data data nya kaya business_status,
# geometry, dsb jadi attributes saja
# Input berupa dict
class Place:
    def __init__(self, results):
        self.address_components = results.get("address_components")
        self.adr_address = results.get("adr_address")
        self.business_status = results.get("business_status")
        self.formatted_address = results.get("formatted_address")
        self.formatted_phone_number = results.get("formatted_phone_number")
        self.geometry = results.get("geometry")
        self.icon = results.get("icon")
        self.icon_background_color = results.get("icon_background_color")
        self.icon_mask_base_uri = results.get("icon_mask_base_uri")
        self.international_phone_number = results.get("international_phone_number")
        self.name = results.get("name")
        self.opening_hours = results.get("opening_hours")
        self.permanently_closed = results.get("permanently_closed")
        self.photos = results.get("photos")
        self.place_id = results.get("place_id")
        self.plus_code = results.get("plus_code")
        self.price_level = results.get("price_level")
        self.rating = results.get("rating")
        self.reference = results.get("reference")
        self.reviews = results.get("reviews")
        self.scope = results.get("scope")
        self.types = results.get("types")
        self.url = results.get("url")
        self.user_ratings_total = results.get("user_ratings_total")
        self.utc_offset = results.get("utc_offset")
        self.vicinity = results.get("vicinity")
        self.website = results.get("website")

    # Unpack geometry attribute to acquire latlong
    def get_latlong(self):
        latlong = [self.geometry["location"]["lat"], self.geometry["location"]["lng"]]
        return latlong


# receives a list of places. returns the centroid of the places based on their latlong
def centroid(places_list):
    total_lat = 0
    total_long = 0
    num_place = len(places_list)
    for i in places_list:
        latlong = i.get_latlong()
        total_lat = total_lat + latlong[0]
        total_long = total_long + latlong[1]
    centroid = [total_lat / num_place, total_long / num_place]
    return centroid


# receives two location (two lists of latlong). returns the haversine distance
def haversine_distance(loc1, loc2):
    distance = hs.haversine(loc1, loc2, unit=Unit.METERS)
    return distance


# receives a list of the places of interest (obj) and a list of user's places (obj). returns the
# top n places of interest (as a suggestion) based on their haversine distance
def distance_based_decision(n, places_of_interest, places_of_users):
    centroid_users = centroid(places_of_users)
    dist_places = (
        []
    )  # placeholder for distance between each places of interests candidate to user's centroid
    top_n_distances_idx = (
        []
    )  # placeholder for top n places (index) with closest distance
    dist_places_untouched = []
    # get the distance from each loc of interests to their centroid
    for i in places_of_interest:
        latlong = i.get_latlong()
        dist_places.append(haversine_distance(latlong, centroid_users))
        dist_places_untouched.append(haversine_distance(latlong, centroid_users))
    # get the top n nearest
    if len(dist_places) < n:
        n = len(dist_places)
    for i in range(n):
        top_n_distances_idx.append(
            dist_places.index(min(dist_places))
        )  # ambil index dist_places dengan nilai minimum
        idx_pop = dist_places.index(min(dist_places))
        dist_places.pop(dist_places.index(min(dist_places)))
        dist_places.insert(idx_pop, max(dist_places) + 1)
    top_n_places_of_interest_short = [
        [
            places_of_interest[i].name,
            str(int(dist_places_untouched[i])) + " meters from centroid",
            places_of_interest[i].formatted_address,
        ]
        for i in top_n_distances_idx
    ]
    top_n_places_of_interest_object = [
        places_of_interest[i] for i in top_n_distances_idx
    ]
    return (
        centroid_users,
        top_n_places_of_interest_short,
        top_n_places_of_interest_object,
    )
