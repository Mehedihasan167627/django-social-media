from django import forms 
from .models import Profile 

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model=Profile 
        fields=["avatar","first_name","last_name","location","profile_info"]