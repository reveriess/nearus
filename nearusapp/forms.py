from django import forms


class UserLocation(forms.Form):
    user_place_1 = forms.CharField(label="Your location 1")
    user_place_2 = forms.CharField(label="Your location 2")
    user_place_3 = forms.CharField(label="Your location 3")
    target_place = forms.CharField(label="Target location")
