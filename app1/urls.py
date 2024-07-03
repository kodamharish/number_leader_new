from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin URL 
    path('',home,name='home'), # Home URL
    path('home',home,name='home'),
    path('about',about,name='about'),
    path('services',services,name='services'),
    path('contact',contact,name='contact'),


    #login,logout
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    #path('sign_up',signup,name='sign_up'),
    path('signup',signup,name='signup'),

    #path('investor_sign_up',investorSignUp,name='investor_sign_up'),
    #path('ca_firm_sign_up',caFirmSignUp,name='ca_firm_sign_up'),

    #Super Admin
    path('super_admin_dashboard',superAdminDashboard,name='super_admin_dashboard'),
    path('admins',admins,name='admins'),
    path('editors',editors,name='editors'),
    path('users',users,name='users'),
    path('startups',startups,name='startups'),
    path('investors',investors,name='investors'),
    path('ca_firms',ca_firms,name='ca_firms'),
    path('companies',companies,name='companies'),


    #Admin
    path('admin_dashboard',adminDashboard,name='admin_dashboard'),
    
    #company
    path('add_company',addCompany,name='add_company'), 
    path('update_company/<str:company_id>/', updateCompany, name='update_company'),
    path('comprehensive_profile/<str:id>/', comprehensiveProfile, name='comprehensive_profile'),
    path('company_profile/<str:id>/',companyProfile,name='company_profile'),
    path('company_profile_form/<str:id>/',companyProfileForm,name='company_profile_form'),
    path('financial_statement/<str:id>/',financialStatement,name='financial_statement'),
    path('revenue_verticals/<str:company_id>/',revenueVerticals,name='revenue_verticals'),

    #children
    path('my_team',myTeam,name='my_team'),
    path('add_team',addTeam,name='add_team'),
    path('update_team/<str:id>',updateTeam,name='update_team'),
    path('delete_team/<str:id>',deleteTeam,name='delete_team'),

    path('parent',parent,name='parent'),
    path('profit_loss_balance_sheet',profitLossBalanceSheetCalculation,name='profit_loss_balance_sheet'),

    #editor
    path('editor_dashboard',editorDashboard,name='editor_dashboard'),
    #user
    path('user_dashboard',userDashboard,name='user_dashboard'),

    #password reset
    path('forgot_password_1',forgotPasswordOne,name='forgot_password_1'),
    path('forgot_password_2',forgotPasswordTwo,name='forgot_password_2'),

]