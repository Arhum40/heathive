from django.urls import path
from .views import (DonorRegisterView, FundraiserRegisterView, WelcomeView, LogoutView, HomePageView, CustomLoginView,
AdminPortalView, FundraiserPortalView, DonorPortalView, FundraiserProfileView,
FundraiserCampaignListView, FundraiserCampaignCreateView,  AdminCampaignApproveView,
DonorProfileView, DonorProfileUpdateView, FundraiserProfileUpdateView,
DonationCreateView, CampaignDetailView)

from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/donor/', DonorRegisterView.as_view(), name='donor_register'),
    path('register/fundraiser/', FundraiserRegisterView.as_view(), name='fundraiser_register'),
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 

    path('admin-portal/', AdminPortalView.as_view(), name='admin_portal'),
    path('fundraiser-portal/', FundraiserPortalView.as_view(), name='fundraiser_portal'),  # Fundraiser portal view
    path('donor-portal/', DonorPortalView.as_view(), name='donor_portal'),


    path('fundraiser/profile/', FundraiserProfileView.as_view(), name='fundraiser_profile'),
    path('fundraiser/profile/update/', FundraiserProfileUpdateView.as_view(), name='fundraiser_profile_update'),
    path('donor/profile/', DonorProfileView.as_view(), name='donor_profile'),
    path('donor/profile/update/', DonorProfileUpdateView.as_view(), name='donor_profile_update'),

   


    path('donate/<int:pk>/', DonationCreateView.as_view(), name='donate_to_campaign'),
    path('campaign/<int:pk>/', CampaignDetailView.as_view(), name='campaign_detail'),


    path('create/', FundraiserCampaignCreateView.as_view(), name='create_campaign'),
    path('fundraiser/campaigns/', FundraiserCampaignListView.as_view(), name='fundraiser_portal'),
    

    path('custom_admin/campaigns/', AdminPortalView.as_view(), name='admin_portal'),  
    path('custom_admin/campaigns/approve/<int:pk>/', AdminCampaignApproveView.as_view(), name='admin_campaign_approve'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)