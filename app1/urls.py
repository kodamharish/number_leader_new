from django.urls import path
from .views import *

urlpatterns = [
    
    path('',home,name='home'),
    path('home',home,name='home'),
    path('about',about,name='about'),

    #login,logout
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('sign_up',signup,name='sign_up'),
    path('sign_up_new',sign_up_new,name='sign_up_new'),

    #path('investor_sign_up',investorSignUp,name='investor_sign_up'),
    #path('ca_firm_sign_up',caFirmSignUp,name='ca_firm_sign_up'),


    #Admin
    path('admin_dashboard',adminDashboard,name='admin_dashboard'),
    path('my_company',myCompany,name='my_company'), 
    #children
    path('my_team',myTeam,name='my_team'),
    path('add_team',addTeam,name='add_team'),
    path('update_team/<str:id>',updateTeam,name='update_team'),
    path('delete_team/<str:id>',deleteTeam,name='delete_team'),

    path('parent',parent,name='parent'),


    
    path('company_profile/<str:id>/',companyProfile,name='company_profile'),
    
    #editor
    path('editor_dashboard',editorDashboard,name='editor_dashboard'),
    #user
    path('user_dashboard',userDashboard,name='user_dashboard'),

    #password reset
    path('forgot_password_1',forgotPasswordOne,name='forgot_password_1'),
    path('forgot_password_2',forgotPasswordTwo,name='forgot_password_2'),






]