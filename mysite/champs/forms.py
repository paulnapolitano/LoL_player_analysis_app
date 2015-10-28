from django import forms

class NameForm(forms.Form):
    summoner_name = forms.CharField(label="Summoner Name", max_length=100)