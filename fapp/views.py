from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView
from .forms import DonorModelForm, FundraiserModelForm, DonorUpdateForm, FundraiserUpdateForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from fapp.models import Fundraiser, Campaign, Donor
from django.contrib.auth.views import LogoutView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.core.mail import send_mail








class HomePageView(ListView):
    model = Campaign
    template_name = 'home.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
       
        return Campaign.objects.filter(status='Active')




class WelcomeView(TemplateView):
    template_name = 'welcome.html'




class DonorRegisterView(CreateView):
    form_class = DonorModelForm
    template_name = 'donor_register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])  
        user.save()
        send_mail(
            'Welcome to HeartHive as a Donor!',
            f'Hi {user.first_name},\n\nThank you for registering as a donor on our platform.',
            'kashifnoor789789@gmail.com',  
            [user.email],   
            fail_silently=False,
        )

        return super().form_valid(form)

class FundraiserRegisterView(CreateView):
    form_class = FundraiserModelForm
    template_name = 'fundraiser_register.html'
    success_url = reverse_lazy('login') 

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password']) 
        user.save()  
        send_mail(
            'Welcome to HeartHive as a Fundraiser!',
            f'Hi {user.first_name},\n\nThank you for registering as a fundraiser on our platform.',
            'kashifnoor789789@gmail.com',  
            [user.email],   
            fail_silently=False,
        )

        return super().form_valid(form)





class AdminPortalView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Campaign
    template_name = 'admin_portal.html'
    context_object_name = 'campaigns'

    def get_queryset(self):
        
        return Campaign.objects.filter(status='Pending Approval')

    def test_func(self):
        
        return self.request.user.is_superuser



class FundraiserPortalView(TemplateView):
    template_name = 'fundraiser_portal.html'


class DonorPortalView(TemplateView):
    template_name = 'donor_portal.html'







class CustomLoginView(LoginView):
    template_name = 'login.html'
    
    def get_success_url(self):
        user = self.request.user

        
        if user.is_superuser:
            return reverse_lazy('admin_portal')
        
       
        elif hasattr(user, 'fundraiser'):
            return reverse_lazy('fundraiser_portal')
        
       
        elif hasattr(user, 'donor'):
            return reverse_lazy('donor_portal')
        
        
        return reverse_lazy('home')
    




class FundraiserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'fundraiser_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        fundraiser = get_object_or_404(Fundraiser, id=self.request.user.id)
        context['fundraiser'] = fundraiser  
        return context


class FundraiserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Fundraiser
    form_class = FundraiserUpdateForm
    template_name = 'fundraiser_profile_update.html'
    success_url = reverse_lazy('fundraiser_profile')  

    def get_object(self):
        return get_object_or_404(Fundraiser, id=self.request.user.id)



class DonorProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'donor_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        donor = get_object_or_404(Donor, id=self.request.user.id)
        context['donor'] = donor  
        return context



class DonorProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Donor
    form_class = DonorUpdateForm
    template_name = 'donor_profile_update.html'
    success_url = reverse_lazy('donor_profile')  

    def get_object(self):
        return get_object_or_404(Donor, id=self.request.user.id)



 
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from .models import Campaign
from .forms import CampaignForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin




class FundraiserCampaignCreateView(LoginRequiredMixin, CreateView):
    model = Campaign
    form_class = CampaignForm
    template_name = 'create_campaign.html'
    success_url = reverse_lazy('fundraiser_portal')

    def form_valid(self, form):
        campaign = form.save(commit=False)
        campaign.fundraiser = self.request.user
        campaign.status = 'Pending Approval'  
        campaign.save()
        return super().form_valid(form)


class FundraiserCampaignListView(LoginRequiredMixin, ListView):
    model = Campaign
    template_name = 'campaign_list.html'
    context_object_name = 'campaigns'

    def get_queryset(self):

        return Campaign.objects.filter(fundraiser=self.request.user)


class AdminCampaignApprovalListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Campaign
    template_name = 'campaign_approval_list.html'
    context_object_name = 'pending_campaigns'

    def get_queryset(self):
        
        return Campaign.objects.filter(status='Pending Approval')

    def test_func(self):
        
        return self.request.user.is_superuser

    




class AdminCampaignApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Campaign
    fields = ['status']  
    template_name = 'campaign_approve.html'
    success_url = reverse_lazy('admin_portal')  

    def test_func(self):
        return self.request.user.is_superuser

    def form_valid(self, form):
        form.instance.status = 'Active'  
        return super().form_valid(form)




from .models import Donation, Campaign
from .forms import DonationForm

    
from django.urls import reverse_lazy

class DonationCreateView(LoginRequiredMixin, CreateView):
    model = Donation
    form_class = DonationForm
    template_name = 'donate.html'


    def form_valid(self, form):
        donation_amount = form.cleaned_data['amount']
        donor = get_object_or_404(Donor, username=self.request.user.username)

        
        campaign = get_object_or_404(Campaign, pk=self.kwargs['pk'])  

        if donor.account_balance >= donation_amount:
           
            donor.account_balance -= donation_amount
            donor.save()

            
            form.instance.donor = donor
            return super().form_valid(form)
        else:
            form.add_error('amount', 'Insufficient balance to make this donation.')
            return self.form_invalid(form)

    def get_success_url(self):
        
        return reverse_lazy('campaign_detail', kwargs={'pk': self.kwargs['pk']})


from django.views.generic import DetailView
from .models import Campaign
from django.db.models import Sum 

class CampaignDetailView(DetailView):
    model = Campaign
    template_name = 'campaign_detail.html'
    context_object_name = 'campaign'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        total_donations = self.object.donation_set.aggregate(Sum('amount'))['amount__sum'] or 0
        context['total_donations'] = total_donations
        return context
    




