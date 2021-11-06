from datetime import datetime
from urllib.parse import urlencode
import base64
import os

import requests

API_KEY = os.environ.get("API_KEY")


def latlong_to_str(latlong):
    return ",".join(str(v) for v in latlong)


# user_latlong=list of lists
def staticmaps_func(user_latlongs, target_latlongs, centroid_users):
    api_url = "https://maps.googleapis.com/maps/api/staticmap?"

    user_markers = ["color:blue", "label:U"] + map(latlong_to_str, user_latlongs)
    target_markers = ["color:red", "label:T"] + map(latlong_to_str, target_latlongs)
    centroid_markers = ["color:yellow", "label:C"] + map(latlong_to_str, centroid_users)

    markers = [
        "|".join(user_markers),
        "|".join(target_markers),
        "|".join(centroid_markers),
    ]

    params = {
        "center": str(centroid_users),
        "size": "500x500",
        "scale": "1",
        "zoom": "12",
        "maptype": "roadmap",
        "style": "feature:poi|visibility:off",
        "key": API_KEY,
        "markers": markers,
    }

    filename = download_to_media(api_url, params)
    data_url = get_media_url(filename)
    return data_url


def download_to_media(url, params):
    response = requests.get(url, params=params)
    now = datetime.now().isoformat()
    filename = f"{now}.png"
    with open(f"media/{filename}", "wb") as f:
        f.write(response.content)
    return filename


def get_media_url(filename):
    return f"/media/{filename}"


def download_as_base64(url, params):
    response = requests.get(url, params=params)
    return base64.b64encode(response.content)


def base64_to_data_uri(base64_str):
    return "data:image/png;base64," + base64_str.decode()
