from django import forms

class NameForm(forms.Form):
    summoner_name = forms.CharField(label='', 
            max_length=100,
            widget=forms.TextInput(attrs={'placeholder':"Enter Summoner Name", 
                                          'size':"21",
                                          'class':"search_bar"}))                               
