
from django import forms
from .models import Donor
from .models import Fundraiser, Campaign, Donation
from django.contrib.auth import get_user_model



class DonorModelForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'contact_info', 'account_balance', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),  
        }






class FundraiserModelForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'contact_info', 'country', 'profile_picture']
        widgets = {
            'password': forms.PasswordInput(),  
        }



class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['title', 'description', 'image', 'deadline', 'target_amount', 'category_id']


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['amount']




class FundraiserUpdateForm(forms.ModelForm):
    class Meta:
        model = Fundraiser
        fields = ['first_name', 'last_name', 'email', 'contact_info', 'country', 'profile_picture']  # Excluding password

class DonorUpdateForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['first_name', 'last_name', 'email', 'contact_info', 'account_balance', 'profile_picture']

