import os

API_KEY = os.environ.get("API_KEY")
# user_latlong=list of lists
def staticmaps_func(staticimg_url, user_latlong, target_latlong, centroid_users):
    markers_str = ""
    num_users = len(user_latlong)
    num_targets = len(target_latlong)
    markers_str = markers_str + "markers=color:blue%7Clabel:U%7C"
    print(markers_str)
    print(user_latlong)
    print(target_latlong)
    print(centroid_users)
    for i in range(num_users):
        counter = 0
        for j in user_latlong[i]:
            counter = counter + 1
            markers_str = markers_str + "".join(str(j))
            if counter == 1:
                markers_str = markers_str + ","
        if i != num_users - 1:
            markers_str = markers_str + "%7C"
    markers_str = markers_str + "&markers=color:red%7Clabel:T%7C"
    for i in range(num_targets):
        counter = 0
        for j in target_latlong[i]:
            counter = counter + 1
            markers_str = markers_str + "".join(str(j))
            if counter == 1:
                markers_str = markers_str + ","
        if i != num_users - 1:
            markers_str = markers_str + "%7C"
    markers_str = (
        markers_str
        + "&markers=color:yellow%7Clabel:C%7C"
        + ",".join([str(c) for c in centroid_users])
    )
    print(markers_str)
    center = "Jakarta"
    size = "size=500x500"
    scale = "scale=1"
    zoom = "zoom=11"
    maptype = "maptype=roadmap"
    style = "style=feature:poi%7Cvisibility:off"
    final_url = (
        staticimg_url
        + size
        + "&"
        + scale
        + "&"
        + zoom
        + "&"
        + maptype
        + "&"
        + style
        + "&"
        + markers_str
        + "&"
        + "key="
        + API_KEY
    )
    return final_url
