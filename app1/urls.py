from django.urls import path
from .views import *

urlpatterns = [
    
    path('',home,name='home'),
    path('home',home,name='home'),
    path('about',about,name='about'),
    path('login_new',login_new,name='login_new'),

    

    #login,logout
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('sign_up',signup,name='sign_up'),
    path('sign_up_new',sign_up_new,name='sign_up_new'),

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
    path('comprehensive_profile', comprehensiveProfile, name='comprehensive_profile'),
    path('company_profile/<str:id>/',companyProfile,name='company_profile'),

    #children
    path('my_team',myTeam,name='my_team'),
    path('add_team',addTeam,name='add_team'),
    path('update_team/<str:id>',updateTeam,name='update_team'),
    path('delete_team/<str:id>',deleteTeam,name='delete_team'),

    path('parent',parent,name='parent'),
    #editor
    path('editor_dashboard',editorDashboard,name='editor_dashboard'),
    #user
    path('user_dashboard',userDashboard,name='user_dashboard'),

    #password reset
    path('forgot_password_1',forgotPasswordOne,name='forgot_password_1'),
    path('forgot_password_2',forgotPasswordTwo,name='forgot_password_2'),






]