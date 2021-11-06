from urllib.parse import urlencode
import os

API_KEY = os.environ.get("API_KEY")
# user_latlong=list of lists
def staticmaps_func(staticimg_url, user_latlong, target_latlong, centroid_users):
    markers_str = ""
    num_users = len(user_latlong)
    num_targets = len(target_latlong)

    # Users' marker
    markers_str = markers_str + "markers=color:blue%7Clabel:U%7C"
    for i in range(num_users):
        counter = 0
        for j in user_latlong[i]:  # user_latlong is a list of list
            counter = counter + 1
            markers_str = markers_str + "".join(str(j))
            if counter == 1:  # comma is inserted between lat and long
                markers_str = markers_str + ","
        if i != num_users - 1:
            markers_str = markers_str + "%7C"  #%7C is inserted between each latlongs
    markers_str = markers_str + "&markers=color:red%7Clabel:T%7C"

    # Targets' marker
    for i in range(num_targets):
        counter = 0
        for j in target_latlong[i]:
            counter = counter + 1
            markers_str = markers_str + "".join(str(j))
            if counter == 1:
                markers_str = markers_str + ","
        if i != num_targets - 1:
            markers_str = markers_str + "%7C"

    # Centroid's marker
    markers_str = (
        markers_str
        + "&markers=color:yellow%7Clabel:C%7C"
        + ",".join([str(c) for c in centroid_users])
    )
    print(markers_str)

    params = {
        "center": str(centroid_users),
        "size": "500x500",
        "scale": "1",
        "zoom": "12",
        "maptype": "roadmap",
        "style": "feature:poi|visibility:off",
        "key": API_KEY,
    }
    strparams = urlencode(params)
    final_url = f"{staticimg_url}{markers_str}&{strparams}"
    return final_url
