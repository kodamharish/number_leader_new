from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from .context_processors import custom_user,custom_subuser
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
#File Handling
from django.utils.deconstruct import deconstructible
from django.core.files.storage import FileSystemStorage
import os

#Mail Configuration
from django.core.mail import send_mail
from numberleader import settings
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact_us.html')


#Login and Logout

# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Check if the user exists in both User and Team models
#         user = User.objects.filter(username=username).first()
#         team = Team.objects.filter(username=username).first()

#         if user:
#             if check_password(password, user.password):
#                 request.session['current_user_id'] = user.user_id
#                 if user.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 if user.user_type == 'super_admin':
#                     return redirect('super_admin_dashboard')
#                 # elif user.user_type == 'editor':
#                 #     return redirect('editor_dashboard')
#                 # elif user.user_type == 'user':
#                 #     return redirect('user_dashboard')
#             else:
#                 messages.error(request, 'Invalid username or password')
#         elif team:
#             if check_password(password, team.password):
#                 request.session['current_subuser_id'] = team.subuser_id
#                 if team.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 elif team.user_type == 'editor':
#                     return redirect('editor_dashboard')
#                 elif team.user_type == 'user':
#                     return redirect('user_dashboard')
#             else:
#                 messages.error(request, 'Invalid username or password')
#         else:
#             messages.error(request, 'Invalid username or password')
#         return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')
    
def login1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                    # return redirect('admin_dashboard')

                else:
                    request.session.set_expiry(0)  # Browser close
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                if user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
               
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
    



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # Get the "Remember Me" value

        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # Uncomment and adjust these lines if needed
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
                if remember_me:
                    request.session.set_expiry(86400)  # 1 day
                else:
                    request.session.set_expiry(0)  # Browser close
                
                if team.user_type == 'admin':
                    return redirect('admin_dashboard')
                elif team.user_type == 'editor':
                    return redirect('editor_dashboard')
                elif team.user_type == 'user':
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
        
        return render(request, 'login.html')
    else:
        return render(request, 'login.html')
def logout(request):
    request.session.flush()
    return redirect('login')

# Sign Up
def signup(request):
    if request.method == 'POST':
        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Company Details
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        company_website_url = request.POST.get('company_website_url')
        company_linkedin_url = request.POST.get('company_linkedin_url')
        subscription_type = request.POST.get('subscription_type')
        company_type = request.POST.get('company_type')
        # Founders Details
        founder_fname = request.POST.get('founder_lname')
        founder_lname = request.POST.get('founder_lname')
        founder_fullname = founder_fname + founder_lname
        founder_email = request.POST.get('founder_email')
        founder_linkedin_url = request.POST.get('founder_linkedin_url')
        founder_phone_number = request.POST.get('founder_phone_number')
        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('signup')    
        # Validate if the username or email already exists
        if User.objects.filter(username=username).exists() or Team.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('signup')    
        if User.objects.filter(email=email).exists() or Team.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('signup')
            
        # Create and save User object
        user = User(
            username=username,
            email=email,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            firstname=firstname,
            lastname=lastname,
            password=password,
            company_type = company_type
        )
        
        user.save()

        # Ensure the user was saved correctly
        if user.pk:
            # Create and save Company object
            company = Company(
                user_id=user,  # This should match the foreign key field in Company model
                name=company_name,
                email=company_email,
                website_url=company_website_url,
                linkedin_url=company_linkedin_url,
                subscription_type = subscription_type
                
            )
            
            company.save()

            # Ensure the company was saved correctly
            if company.pk:
                company_id = Company.objects.get(company_id = company.pk)
                founder =Founder(
                    company_id = company_id,
                    name=founder_fullname,
                    email=founder_email,
                    linkedin_url=founder_linkedin_url,
                    phone_number=founder_phone_number,
                )
                founder.save()
                messages.error(request,'User Created Succesfully')
                return redirect('signup')
                
            else:
                messages.error(request,'Something went wrong please try again later')
                return redirect('signup')
                
        else:
            messages.error(request,'Something went wrong please try again later')
            return redirect('signup')
           
    else:
        return render(request, 'sign_up.html')





#Super Admin
def superAdminDashboard(request):
    admins_count = User.objects.count()
    editors_count = Team.objects.filter(user_type='editor').count()
    users_count = Team.objects.filter(user_type='user').count()

    startups = User.objects.filter(company_type='Startup').count()
    investors= User.objects.filter(company_type='Investor').count()
    ca_firms= User.objects.filter(company_type='CA_firm').count()
    companys = Company.objects.count()
    context = {
        'admins_count': admins_count,
        'editors_count': editors_count,
        'users_count': users_count,
        'startups':startups,
        'investors':investors,
        'ca_firms':ca_firms,
        'companys':companys
    }

    return render(request,'super_admin/dashboard.html',context)


def startups(request):
    startups = User.objects.filter(company_type='Startup').all()
    context = {'startups':startups}
    return render(request,'super_admin/startups.html',context)

def investors(request):
    investors= User.objects.filter(company_type='Investor').all()
    context = {'investors':investors}
    return render(request,'super_admin/investors.html',context)

def ca_firms(request):
    ca_firms= User.objects.filter(company_type='CA_firm').all()
    context = {'ca_firms':ca_firms}
    return render(request,'super_admin/ca_firms.html',context)

def companies(request):
    companies = Company.objects.all()
    context ={'companies':companies}
    return render(request,'super_admin/companies.html',context)

def admins(request):
    admins = User.objects.all()
    context = {'admins':admins}

    return render(request,'super_admin/admins.html',context)

def editors(request):
    editors = Team.objects.filter(user_type='editor')
    context = {'editors':editors}

    return render(request,'super_admin/editors.html',context)

def users(request):
    users = Team.objects.filter(user_type='user')
    context = {'users':users}

    return render(request,'super_admin/users.html',context)




#Admin

def myTeam(request):
    if request.method == 'POST':
        pass          
    else:
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        if current_user:
            total_team_data = Team.objects.filter(creator_id =current_user)
        if current_subuser:
                total_team_data = Team.objects.filter(creator_id = current_subuser)

        context = {'total_team_data':total_team_data}
        return render(request, 'admin/my_team.html',context)

def addTeam(request):
    if request.method == 'POST':
        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        
        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('add_team')
            
        # Validate if the username or email already exists
        if Team.objects.filter(username=username).exists() or User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('add_team')
            
        if Team.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('add_team')
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  
        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 
        #creator_id = current_subuser.creator_id

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id

        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)
        # Create and save User object
        team = Team(
            username=username,
            creator_id=creator_user,
            company_id = company_id,
            email=email,
            phone_number=phone_number,
            linkedin_url=linkedin_url,
            firstname=firstname,
            lastname=lastname,
            password=password,
            user_type = user_type
        )
        
        team.save()
        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader Registration Details'
        txt='''Welcome to  Number Leader

               Below are your Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.error(request,'Member Created Successfully')
        return redirect('add_team')       
           
    else:
        return render(request, 'admin/add_team.html')
    

def updateTeam(request, id):
    if request.method == 'POST':
        # Fetch the existing Team instance using subuser_id
        team = get_object_or_404(Team, subuser_id=id)

        # Extract form data using request.POST.get
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname', '')  # Optional field
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')
        companyID = request.POST.get('company')

        

        user_context = custom_user(request)
        current_user = user_context.get('current_user')  

        # # Fetch the User instance for the creator_id
        # creator_user = User.objects.get(user_id=current_user.user_id)

        subuser_context = custom_subuser(request)
        current_subuser = subuser_context.get('current_subuser') 

        if current_user:
            # Fetch the User instance for the creator_id
              #creator_user = User.objects.get(user_id=current_user.user_id)
              creator_user = current_user.user_id
        if current_subuser:
              if current_subuser.user_type == 'editor':
                  # Fetch the User instance for the creator_id
                  #creator_user = Team.objects.get(subuser_id=current_subuser.subuser_id)
                  creator_user = current_subuser.subuser_id


        
        # Fetch the Company instance based on company_id
        company_id = Company.objects.get(company_id=companyID)

        # Update the Team instance
        team.username = username
        team.creator_id = creator_user
        team.company_id = company_id
        team.email = email
        team.phone_number = phone_number
        team.linkedin_url = linkedin_url
        team.firstname = firstname
        team.lastname = lastname
        team.password = password
        team.user_type = user_type
        
        team.save()

        # Get the current site domain
        current_site = get_current_site(request)
        domain = current_site.domain

        # Construct the Login URL
        signin_url = f'http://{domain}/login'

        subject='Number Leader - Updated Details'
        txt='''Welcome to  Number Leader

               Below are your Updated Login Details :

               First Name : {}
               First Name : {}
               Email : {}
               Username : {}
               Password : {}
               Phone Number : {}
               Linkedin URL : {}
               User Type : {}
               Company : {}

               You can Login by using below this URL : {}        
                '''
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.company_name,signin_url)
        from_email=settings.EMAIL_HOST_USER
        to_list=[email]
        send_mail(subject, message,from_email,to_list,fail_silently=True)
        messages.success(request, 'Member Updated Successfully')
        return redirect('add_team')       
    else:
        context={'team': get_object_or_404(Team, subuser_id=id)}
        return render(request, 'admin/update_team.html',context)

def deleteTeam(request,id):
    team = get_object_or_404(Team, subuser_id=id)    
    # Delete the team member
    team.delete()
    # Show a success message
    messages.success(request, 'Member Deleted Successfully')
    return redirect('my_team')
 

def adminDashboard(request):
    return render(request,'admin/dashboard.html')



# def addCompany(request):
#     if request.method == 'POST':
#         # Extract company profile data
#         startup_name = request.POST.get('startup_name')
#         sector = request.POST.get('sector')
#         subscription_type = request.POST.get('subscription_type')
#         website_url = request.POST.get('website_url')
#         business_introductory_video = request.FILES.get('business_introductry_video')
#         business_plan = request.FILES.get('business_plan')
#         vision = request.POST.get('vision')
#         mission = request.POST.get('mission')
#         usp = request.POST.get('usp')

#         user_context = custom_user(request)
#         current_user = user_context.get('current_user') 

#         # Create the Company instance
#         company = Company(
#                 user_id=current_user,  # This should match the foreign key field in Company model
#                 name=startup_name,
#                 # company_email=company_email,
#                 website_url=website_url,
#                 # linkedin_url=linkedin_url,
#                 subscription_type=subscription_type,
#             )
#         company.save()
#         company_profile = CompanyProfile(
#             company_id = company,
#             sector=sector,
#             business_introductory_video = business_introductory_video,
#             business_plan = business_plan,
#             vision = vision,
#             mission = mission,
#             usp = usp
#         )
#         company_profile.save()

#         # Save founders
#         founder_count = int(request.POST.get('founder_count', 1))
#         for i in range(1, founder_count + 1):
#             founder_name = request.POST.get(f'founder{i}_name')
#             linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
#             short_profile = request.POST.get(f'founder{i}_short_profile')
#             phone_no = request.POST.get(f'founder{i}_phone_no')
#             email = request.POST.get(f'founder{i}_email')
#             photo = request.FILES.get(f'founder{i}_photo')
#             if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
#                 founder = Founder(
#                     company_id=company,
#                     name=founder_name,
#                     linkedin_url=linkedin_profile,
#                     short_profile=short_profile,
#                     phone_number=phone_no,
#                     email=email,
#                     photo=photo
#                 )
#                 founder.save()

#         # Save social media URLs
#         url_count = int(request.POST.get('url_count', 2))
#         for i in range(1, url_count + 1):
#             url = request.POST.get(f'url_{i}')
#             if url:

#                 socail_media = SocialMedia(
#                     company_id=company,
#                     url=url
#                 )
#                 socail_media.save()

#         # Save clients
#         client_count = int(request.POST.get('client_count', 2))
#         for i in range(1, client_count + 1):
#             client_name = request.POST.get(f'client_{i}')
#             client_logo = request.POST.get(f'client_{i}_logo')

#             if client_name:
                
#                 client = Client(
#                     company_id=company,
#                     name=client_name,
#                     logo = client_logo
#                 )
#                 client.save()

#         return redirect('add_company')  # Redirect to a success page
#     else:
#         return render(request, 'admin/add_company.html')



def addCompany(request):
    if request.method == 'POST':
        # Extract company profile data
        startup_name = request.POST.get('startup_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video_file = request.FILES.get('business_introductry_video_file')
        business_introductory_video_url = request.POST.get('business_introductry_video_url')

        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        # Create the Company instance
        company = Company(
            user_id=current_user,  # This should match the foreign key field in Company model
            name=startup_name,
            website_url=website_url,
            subscription_type=subscription_type,
        )
        company.save()

        # Create the CompanyProfile instance
        company_profile = CompanyProfile(
            company_id=company,
            sector=sector,
            business_introductory_video_file=business_introductory_video_file,
            business_introductory_video_url=business_introductory_video_url,
            business_plan=business_plan,
            vision=vision,
            mission=mission,
            usp=usp
        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=company,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                social_media = SocialMedia(
                    company_id=company,
                    url=url
                )
                social_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 1))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')
            if client_name and client_logo:
                client = Client(
                    company_id=company,
                    name=client_name,
                    logo=client_logo
                )
                client.save()

        return redirect('add_company')  # Redirect to a success page
    else:
        return render(request, 'admin/add_company.html')


def updateCompanyOld(request, company_id):
    if request.method == 'POST':
        # Fetch existing company and profile
        company = get_object_or_404(Company, company_id=company_id)
        company_profile = get_object_or_404(CompanyProfile, company_id=company_id)
        

        
        # Company Details
        company.company_name = request.POST.get('company_name')
        company.company_email = request.POST.get('company_email')
        company.company_website_url = request.POST.get('company_website_url')
        company.company_linkedin_url = request.POST.get('company_linkedin_url')
        company.subscription_type = request.POST.get('subscription_type')
        
        # Founders Details
        company.founder_name = request.POST.get('founder_name')
        company.founder_email = request.POST.get('founder_email')
        company.founder_linkedin_url = request.POST.get('founder_linkedin_url')
        company.founder_phone_number = request.POST.get('founder_phone_number')
        
        # Company profile
        company_profile.excecutive_summary = request.POST.get('excecutive_summary')
        company_profile.technology_profile = request.POST.get('technology_profile')
        company_profile.type_of_industry = request.POST.get('type_of_industry')
        company_profile.no_of_employees = request.POST.get('no_of_employees')
        company_profile.ceo = request.POST.get('ceo')
        company_profile.cfo = request.POST.get('cfo')
        company_profile.cmo = request.POST.get('cmo')
        company_profile.vp = request.POST.get('vp')

        
        
        # Save the updates
        company.save()
        company_profile.save()
        

        messages.success(request, 'Data updated successfully')
        return redirect('update_company', company_id=company_id)
    else:
        # Fetch existing company and profile for initial form rendering
        company = get_object_or_404(Company, company_id=company_id)
        company_profile = get_object_or_404(CompanyProfile, company_id=company_id)
        

        context = {
            'company': company,
            'company_profile': company_profile,
           
        }
        
        return render(request, 'admin/update_company.html', context)




def updateCompany_ref(request,id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    founders = Founder.objects.filter(company_id = id)
    clients = Client.objects.filter(company_id = id)
    socail_media_urls = SocialMedia.objects.filter(company_id = id)

    if request.method == 'POST':
        # Extract company profile data
        startup_name = request.POST.get('startup_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video = request.FILES.get('business_introductry_video')
        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user')
        # Create the Company instance
        company = Company(
                user_id=current_user,  # This should match the foreign key field in Company model
                name=startup_name,
                # company_email=company_email,
                website_url=website_url,
                # linkedin_url=linkedin_url,
                subscription_type=subscription_type,
            )
        company.save()
        company_profile = CompanyProfile(
            company_id = id,
            sector=sector,
            business_introductory_video = business_introductory_video,
            business_plan = business_plan,
            vision = vision,
            mission = mission,
            usp = usp
        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=id,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:

                socail_media = SocialMedia(
                    company_id=id,
                    url=url
                )
                socail_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 2))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            if client_name:
                
                client = Client(
                    company_id=id,
                    name=client_name
                )
                client.save()

        return redirect('admin_dashboard')  # Redirect to a success page
    else:
        context = {
            'company':company,
            'company_profile':company_profile,
            'founders':founders,
            'clients':clients,
            'socail_media_urls':socail_media_urls
        }
        return render(request, 'admin/update_company.html',context)



from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import MultipleObjectsReturned

def updateCompany12(request, id):
    company = get_object_or_404(Company, company_id=id)
    company_profile = get_object_or_404(CompanyProfile, company_id=id)
    founders = Founder.objects.filter(company_id=id)
    clients = Client.objects.filter(company_id=id)
    social_media_urls = SocialMedia.objects.filter(company_id=id)

    if request.method == 'POST':
        # Extract company profile data
        startup_name = request.POST.get('startup_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video = request.FILES.get('business_introductory_video')
        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        # Update the Company instance
        company.name = startup_name
        company.website_url = website_url
        company.subscription_type = subscription_type
        company.save()

        # Update the CompanyProfile instance
        company_profile.sector = sector
        if business_introductory_video:
            company_profile.business_introductory_video = business_introductory_video
        if business_plan:
            company_profile.business_plan = business_plan
        company_profile.vision = vision
        company_profile.mission = mission
        company_profile.usp = usp
        company_profile.save()

        # Update founders
        founder_count = int(request.POST.get('founder_count', founders.count()))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')

            # if founder_name and linkedin_profile and short_profile and phone_no and email:
            #     founder_instances = Founder.objects.filter(company_id=id, name=founder_name)
            #     for founder in founder_instances:
            #         founder.name = founder_name
            #         founder.linkedin_url = linkedin_profile
            #         founder.short_profile = short_profile
            #         founder.phone_number = phone_no
            #         founder.email = email
            #         if photo:
            #             founder.photo = photo
            #         founder.save()
            if founder_name and linkedin_profile and short_profile and phone_no and email:
                founder_instances = Founder.objects.filter(company_id=id)
                for founder in founder_instances:
                    founder.name = founder_name
                    founder.linkedin_url = linkedin_profile
                    founder.short_profile = short_profile
                    founder.phone_number = phone_no
                    founder.email = email
                    if photo:
                        founder.photo = photo
                    founder.save()

        # Update social media URLs
        # url_count = int(request.POST.get('url_count', social_media_urls.count()))
        # for i in range(1, url_count + 1):
        #     url = request.POST.get(f'url_{i}')
        #     if url:
        #         social_media_instances = SocialMedia.objects.filter(company_id=id, url=url)
        #         for social_media in social_media_instances:
        #             social_media.url = url
        #             social_media.save()
        url_count = int(request.POST.get('url_count', social_media_urls.count()))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            social_media_instances = SocialMedia.objects.filter(company_id=id)
            for social_media in social_media_instances:
                        social_media.url = url
                        social_media.save()

        # Update clients
        # client_count = int(request.POST.get('client_count', clients.count()))
        # for i in range(1, client_count + 1):
        #     client_name = request.POST.get(f'client_{i}')
        #     if client_name:
        #         client_instances = Client.objects.filter(company_id=id, name=client_name)
        #         for client in client_instances:
        #             client.name = client_name
        #             client.save()
        client_count = int(request.POST.get('client_count', clients.count()))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')

            client_instances = Client.objects.filter(company_id=id)
            for client in client_instances:
                    client.name = client_name
                    client.logo = client_logo
                    client.save()

        return redirect('admin_dashboard')  # Redirect to a success page
    else:
        context = {
            'company': company,
            'company_profile': company_profile,
            'founders': founders,
            'clients': clients,
            'social_media_urls': social_media_urls
        }
        return render(request, 'admin/update_company.html', context)



from django.shortcuts import get_object_or_404, redirect, render
from .models import Company, CompanyProfile, Founder, SocialMedia, Client

def updateCompany11(request, id):
    company = get_object_or_404(Company, company_id=id)
    company_profile = get_object_or_404(CompanyProfile, company_id=id)
    founders = Founder.objects.filter(company_id=id)
    clients = Client.objects.filter(company_id=id)
    social_media_urls = SocialMedia.objects.filter(company_id=id)

    if request.method == 'POST':
        # Extract company profile data
        startup_name = request.POST.get('startup_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video_file = request.FILES.get('business_introductory_video_file')
        business_introductory_video_url = request.POST.get('business_introductory_video_url')

        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        # Update the Company instance
        company.name = startup_name
        company.website_url = website_url
        company.subscription_type = subscription_type
        company.save()

        # Update the CompanyProfile instance
        company_profile.sector = sector
        if business_introductory_video_file:
            company_profile.business_introductory_video_file = business_introductory_video_file
        if business_plan:
            company_profile.business_plan = business_plan
        company_profile.vision = vision
        company_profile.mission = mission
        company_profile.usp = usp
        company_profile.save()

        # Update founders
        founder_count = int(request.POST.get('founder_count', founders.count()))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')

            founder_instances = Founder.objects.filter(company_id=id)
            for founder in founder_instances:
                founder.name = founder_name
                founder.linkedin_url = linkedin_profile
                founder.short_profile = short_profile
                founder.phone_number = phone_no
                founder.email = email
                if photo:
                    founder.photo = photo
                founder.save()

        # Update social media URLs
        url_count = int(request.POST.get('url_count', social_media_urls.count()))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            social_media_instances = SocialMedia.objects.filter(company_id=id)
            for social_media in social_media_instances:
                social_media.url = url
                social_media.save()

        # Update clients
        client_count = int(request.POST.get('client_count', clients.count()))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')

            client_instances = Client.objects.filter(company_id=id)
            for client in client_instances:
                client.name = client_name
                if client_logo:
                    client.logo = client_logo
                client.save()

        return redirect('admin_dashboard')  # Redirect to a success page
    else:
        context = {
            'company': company,
            'company_profile': company_profile,
            'founders': founders,
            'clients': clients,
            'social_media_urls': social_media_urls
        }
        return render(request, 'admin/update_company.html', context)



from django.shortcuts import get_object_or_404, redirect, render
from .models import Company, CompanyProfile, Founder, SocialMedia, Client

def updateCompany(request, id):
    company = get_object_or_404(Company, company_id=id)
    company_profile = get_object_or_404(CompanyProfile, company_id=id)
    founders = Founder.objects.filter(company_id=id)
    clients = Client.objects.filter(company_id=id)
    social_media_urls = SocialMedia.objects.filter(company_id=id)

    if request.method == 'POST':
        # Extract company profile data
        startup_name = request.POST.get('startup_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video_file = request.FILES.get('business_introductory_video_file')
        business_introductory_video_url = request.POST.get('business_introductory_video_file')
        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        # Update the Company instance
        company.name = startup_name
        company.website_url = website_url
        company.subscription_type = subscription_type
        company.save()

        # Update the CompanyProfile instance
        company_profile.sector = sector
        if business_introductory_video_file:
            company_profile.business_introductory_video_file = business_introductory_video_file
        if business_introductory_video_url:
            company_profile.business_introductory_video_url = business_introductory_video_url
        if business_plan:
            company_profile.business_plan = business_plan
        company_profile.vision = vision
        company_profile.mission = mission
        company_profile.usp = usp
        company_profile.save()

        # Update founders
        founder_count = int(request.POST.get('founder_count', founders.count()))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')

            if founder_name and linkedin_profile and short_profile and phone_no and email:
                if i <= len(founders):
                    founder = founders[i - 1]
                    founder.name = founder_name
                    founder.linkedin_url = linkedin_profile
                    founder.short_profile = short_profile
                    founder.phone_number = phone_no
                    founder.email = email
                    if photo:
                        founder.photo = photo
                    founder.save()

        # Update social media URLs
        url_count = int(request.POST.get('url_count', social_media_urls.count()))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:
                if i <= len(social_media_urls):
                    social_media = social_media_urls[i - 1]
                    social_media.url = url
                    social_media.save()

        # Update clients
        client_count = int(request.POST.get('client_count', clients.count()))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')

            if client_name:
                if i <= len(clients):
                    client = clients[i - 1]
                    client.name = client_name
                    if client_logo:
                        client.logo = client_logo
                    client.save()

        return redirect('admin_dashboard')  # Redirect to a success page
    else:
        context = {
            'company': company,
            'company_profile': company_profile,
            'founders': founders,
            'clients': clients,
            'social_media_urls': social_media_urls
        }
        return render(request, 'admin/update_company.html', context)


def companyProfileFormOld(request,id):
    company = get_object_or_404(Company, company_id=id)

    # user_context = custom_subuser(request)
    # user = user_context.get('current_user') 
    # company = Company.objects.get(company_id =user.company_id)
    if request.method == 'POST':
            # Company profile
            excecutive_summary = request.POST.get('excecutive_summary')
            technology_profile = request.POST.get('technology_profile')
            type_of_industry = request.POST.get('type_of_industry')
            no_of_employees = request.POST.get('no_of_employees')
            ceo = request.POST.get('ceo')
            cfo = request.POST.get('cfo')
            cmo = request.POST.get('cmo')
            vp = request.POST.get('vp')
            date_of_inc = request.POST.get('date_of_inc')
            # Create the CompanyProfile instance and associate it with the Company instance
            company_profile = CompanyProfile(
            company_id=company,  # Associate with the newly created Company instancec
            excecutive_summary=excecutive_summary,
            technology_profile=technology_profile,
            type_of_industry=type_of_industry,
            no_of_employees=no_of_employees,
            ceo=ceo,
            cfo=cfo,
            cmo=cmo,
            vp=vp
            )
            company_profile.save()

             # Convert the date_of_inc string to a datetime object
            date_of_inc_dt = datetime.strptime(date_of_inc, '%Y-%m-%d')
            today = datetime.now()
            # Calculate the difference in years between today and date_of_inc_dt
            years_difference = relativedelta(today, date_of_inc_dt).years
             # Check if the difference is less than 2 years
            if years_difference < 2:
                return redirect('financial_statement',id)  # Redirect to signup page if less than 2 years

            # # Check if the date of incorporation is less than two years from today
            # if relativedelta(today, date_of_inc_dt).years < 2:
            #     return redirect('financial_statement')

            messages.success(request, 'Data saved Successfully')
            return redirect('update_company',id)
    else:
        return render(request, 'admin/company_profile_form.html')




def companyProfileForm(request,id):
    #company = get_object_or_404(Company, company_id=id)
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        # Extract company profile data
        excecutive_summary = request.POST.get('excecutive_summary')
        technology_profile = request.POST.get('technology_profile')
        no_of_employees = request.POST.get('no_of_employees')
        startup_name = request.POST.get('start_name')
        sector = request.POST.get('sector')
        subscription_type = request.POST.get('subscription_type')
        website_url = request.POST.get('website_url')
        business_introductory_video_file = request.FILES.get('business_introductry_video_file')
        business_introductory_video_url = request.POST.get('business_introductry_video_url')

        business_plan = request.FILES.get('business_plan')
        vision = request.POST.get('vision')
        mission = request.POST.get('mission')
        usp = request.POST.get('usp')

        user_context = custom_user(request)
        current_user = user_context.get('current_user') 

        # Create the Company instance
        # company = Company(
        #         user_id=current_user,  # This should match the foreign key field in Company model
        #         name=startup_name,
        #         # company_email=company_email,
        #         website_url=website_url,
        #         # linkedin_url=linkedin_url,
        #         subscription_type=subscription_type,
        #     )
        # company.save()
        company_profile = CompanyProfile(
            company_id = company,
            excecutive_summary = excecutive_summary,
            technology_profile = technology_profile,
            no_of_employees = no_of_employees,
            sector=sector,
            business_introductory_video_file = business_introductory_video_file,
            business_introductory_video_url = business_introductory_video_url,

            business_plan = business_plan,
            vision = vision,
            mission = mission,
            usp = usp
        )
        company_profile.save()

        # Save founders
        founder_count = int(request.POST.get('founder_count', 1))
        for i in range(1, founder_count + 1):
            founder_name = request.POST.get(f'founder{i}_name')
            linkedin_profile = request.POST.get(f'founder{i}_linkedin_profile')
            short_profile = request.POST.get(f'founder{i}_short_profile')
            phone_no = request.POST.get(f'founder{i}_phone_no')
            email = request.POST.get(f'founder{i}_email')
            photo = request.FILES.get(f'founder{i}_photo')
            if founder_name and linkedin_profile and short_profile and phone_no and email and photo:
                founder = Founder(
                    company_id=company,
                    name=founder_name,
                    linkedin_url=linkedin_profile,
                    short_profile=short_profile,
                    phone_number=phone_no,
                    email=email,
                    photo=photo
                )
                founder.save()

        # Save social media URLs
        url_count = int(request.POST.get('url_count', 2))
        for i in range(1, url_count + 1):
            url = request.POST.get(f'url_{i}')
            if url:

                socail_media = SocialMedia(
                    company_id=company,
                    url=url
                )
                socail_media.save()

        # Save clients
        client_count = int(request.POST.get('client_count', 1))
        for i in range(1, client_count + 1):
            client_name = request.POST.get(f'client_{i}')
            client_logo = request.FILES.get(f'client_{i}_logo')
            if client_name and client_logo:
                client = Client(
                    company_id=company,
                    name=client_name,
                    logo=client_logo
                )
                client.save()



        return redirect('admin_dashboard')  # Redirect to a success page
    
    else:
        return render(request, 'admin/company_profile_form.html')


def companyProfile(request, id):
    company = get_object_or_404(Company, company_id=id)
    try:
        company_profile = CompanyProfile.objects.get(company_id=id)
    except CompanyProfile.DoesNotExist:
        company_profile = None

    

    if request.method == 'POST':
            # Company profile
            excecutive_summary = request.POST.get('excecutive_summary')
            technology_profile = request.POST.get('technology_profile')
            type_of_industry = request.POST.get('type_of_industry')
            no_of_employees = request.POST.get('no_of_employees')
            ceo = request.POST.get('ceo')
            cfo = request.POST.get('cfo')
            cmo = request.POST.get('cmo')
            vp = request.POST.get('vp')
            # Create the CompanyProfile instance and associate it with the Company instance
            company_profile = CompanyProfile(
            company_id=company,  # Associate with the newly created Company instancec
            excecutive_summary=excecutive_summary,
            technology_profile=technology_profile,
            type_of_industry=type_of_industry,
            no_of_employees=no_of_employees,
            ceo=ceo,
            cfo=cfo,
            cmo=cmo,
            vp=vp
            )
            company_profile.save()

            
            messages.success(request, 'Data saved Successfully')
            return redirect('comprehensive_profile')
    else:
        context = {'company': company,'company_profile': company_profile }
        return render(request, 'admin/company_profile.html', context)
    

def comprehensiveProfile(request,id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    context ={'company_profile': company_profile}

    return render(request, 'admin/comprehensive.html', context)



def basicInformation(request,id):
    company = Company.objects.get(company_id = id)
    company_profile = CompanyProfile.objects.get(company_id = id)
    founders = Founder.objects.filter(company_id = id)
    clients = Client.objects.filter(company_id = id)


   
    context = {
        'company':company,
        'company_profile': company_profile,
        'founders':founders,
        'clients':clients
    }
    return render(request,'admin/basic_information.html',context)

def businessPlan(request, id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    
   
    context = {
        'company_profile': company_profile,
    }

    return render(request, 'admin/business_plan.html', context)

def capTable(request, id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    cap_table = CapTable.objects.filter(company_id = id)
    context = {'company_profile': company_profile,'cap_table': cap_table }
   

    return render(request, 'admin/cap_table.html', context)

def capTableForm(request, id):
    company = Company.objects.get(company_id = id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        linkedin_url = request.POST.get('linkedin_url')
        percentage_of_shares = request.POST.get('percentage_of_shares')
        photo = request.FILES.get('photo')

        cap_table = CapTable(
            company_id = company,
            name = name,
            email = email,
            linkedin_url = linkedin_url,
            percentage_of_shares = percentage_of_shares,
            photo = photo
        )
        cap_table.save()
        messages.success(request,'Data saved successfully')
        return redirect('cap_table',company.company_id)

    else:
        company_profile = CompanyProfile.objects.get(company_id = id)
        context ={'company_profile': company_profile}
    
        context = {
            'company_profile': company_profile,
        }

        return render(request, 'admin/cap_table_form.html', context)



def financialStatement(request,id):
    company_profile = CompanyProfile.objects.get(company_id = id)
    homogenous_products = HomogenousProduct.objects.filter(company_id = id)
    heterogenous_products = HeterogenousProduct.objects.filter(company_id = id)
    context ={'company_profile': company_profile,'homogenous_products':homogenous_products,'heterogenous_products':heterogenous_products}

    return render(request,'admin/financial_statement.html',context)






#New one
def revenueVerticals(request, company_id):
    company_id = Company.objects.get(company_id = company_id)
    if request.method == 'POST':
        # Process homogenous products if any
        homogenous_product_names = request.POST.getlist('homogenous_product_name[]')
        homogenous_selling_prices = request.POST.getlist('homogenous_selling_price_per_unit[]')
        homogenous_units_sold = request.POST.getlist('homogenous_units_sold[]')
        homogenous_growth_rates = request.POST.getlist('homogenous_expected_growth_rate[]')

        for name, price, units, growth in zip(homogenous_product_names, homogenous_selling_prices, homogenous_units_sold, homogenous_growth_rates):
            if name and price and units and growth:
                HomogenousProduct.objects.create(
                   company_id = company_id,
                product_name = name,
                selling_price_per_unit = price,
                units_sold = units,
                expected_growth_rate = growth
                )

        # Process heterogenous products if any
        heterogenous_product_names = request.POST.getlist('heterogenous_product_name[]')
        heterogenous_expected_revenues = request.POST.getlist('heterogenous_expected_revenue[]')
        heterogenous_growth_rates = request.POST.getlist('heterogenous_expected_growth_rate[]')

        for name, revenue, growth in zip(heterogenous_product_names, heterogenous_expected_revenues, heterogenous_growth_rates):
            if name and revenue and growth:
                HeterogenousProduct.objects.create(
                    company_id=company_id,
                    product_name = name,
                expected_revenue = revenue,
                expected_growth_rate = growth
                )
        
        return redirect('revenue_verticals',company_id)  # Change to your desired redirect URL
    else:
        # Handle GET request or any other logic here
        company_profile = CompanyProfile.objects.get(company_id = company_id)
        context ={'company_profile': company_profile}
        return render(request, 'admin/revenue_verticals.html', context)


def expenses(request,company_id):
    if request.method == 'POST':
        pass
    else:
        # Handle GET request or any other logic here
        company_profile = CompanyProfile.objects.get(company_id = company_id)
        context ={'company_profile': company_profile}
        return render(request,'admin/expenses.html',context)
    
def profitLossBalanceSheetCalculation(request):
    if request.method == 'POST':
        company_id = request.POST.get('company_id')
        revenue_recurring = request.POST.get('revenue_recurring')
        revenue_one_time = request.POST.get('revenue_one_time')
        other_income = request.POST.get('other_income')
        total_income = request.POST.get('total_income')

        cost_of_materials_consumed = request.POST.get('cost_of_materials_consumed')
        changes_inventories_of_fg_wip = request.POST.get('changes_inventories_of_fg_wip')
        emp_benefits_expenses = request.POST.get('emp_benefits_expenses')
        depreciation_amortization_expenses = request.POST.get('depreciation_amortization_expenses')
        finance_cost = request.POST.get('finance_cost')
        other_expenses = request.POST.get('other_expenses')
        total_expenses = request.POST.get('total_expenses')

        profit_before_tax = request.POST.get('profit_before_tax')
        current_tax_expense = request.POST.get('current_tax_expense')
        deferred_tax = request.POST.get('deferred_tax')
        profit_after_tax = request.POST.get('profit_after_tax')

        companyId = Company.objects.get(company_id=company_id)

        profit_loss_balance_sheet = ProfitLossBalanceSheet(
            company_id = companyId,
            revenue_recurring = revenue_recurring,
            revenue_one_time = revenue_one_time,
            other_income = other_income,
            total_income = total_income,
            cost_of_materials_consumed = cost_of_materials_consumed,
            changes_inventories_of_fg_wip = changes_inventories_of_fg_wip,
            emp_benefits_expenses = emp_benefits_expenses,
            depreciation_amortization_expenses = depreciation_amortization_expenses,
            finance_cost = finance_cost,
            other_expenses = other_expenses,
            total_expenses = total_expenses,
            profit_before_tax = profit_before_tax,
            current_tax_expense = current_tax_expense,
            deferred_tax = deferred_tax,
            profit_after_tax = profit_after_tax

        )

        profit_loss_balance_sheet.save()
        messages.success(request,'Data Saved Successfully')
        return redirect('profit_loss_balance_sheet')
    else:
        return render(request,'admin/profit_loss_balance_sheet_form.html')
    
#Editor
def editorDashboard(request):
    return render(request,'editor/dashboard.html')

def parent(request):
    subuser_context = custom_subuser(request)
    current_subuser = subuser_context.get('current_subuser') 
    creator_id = current_subuser.creator_id
    creator_data=User.objects.get(user_id = creator_id)
    context ={'creator_data':creator_data}
    return render(request,'editor/parent.html',context)

#User
def userDashboard(request):
    return render(request,'user/dashboard.html')

#Password Reset 
import random
def generate_random_otp():
    otp = ""
    for i in range(5):
        otp += str(random.randint(0, 9))
    return otp
#generate_random_otp()
#print("Generated OTP:", generate_otp())

def forgotPasswordOne(request):
    if request.method == 'POST':
        input_email = request.POST['email']
        print(input_email)
        if User.objects.filter(email=input_email).exists() or Team.objects.filter(email=input_email).exists():
            generated_otp = generate_random_otp()
            request.session['OTP'] = generated_otp
            request.session['email'] = input_email
            # Debug print statements
            # print("OTP set in session:", request.session.get('OTP'))
            # print("Email set in session:", request.session.get('email'))
            # Get the current site domain
            current_site = get_current_site(request)
            domain = current_site.domain

            # Construct the signin URL
            password_reset_url = f'http://{domain}/forgot_password_2'

            subject='Number Leader - Password Reset Link'
            txt='''
                Password Reset Link and OTP :

                OTP: {}
                Domain: {}

                    '''
            message=txt.format(generated_otp,password_reset_url)
            from_email=settings.EMAIL_HOST_USER
            to_list=[input_email]
            send_mail(subject, message,from_email,to_list,fail_silently=True)
            messages.success(request,'we have sent opt to your mail please check')
            return redirect('forgot_password_1')
        else:
            messages.error(request,'please enter the registered email')
            return redirect('forgot_password_1')
    else:
        return render(request,'forgot_password_1.html')


def forgotPasswordTwo(request):
    if request.method == 'POST':
        input_otp = int(request.POST['otp'])
        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        session_otp = request.session.get('OTP')
        session_email =request.session.get('email')
        

        if 'OTP' in request.session and 'email' in request.session:
            if input_otp == int(session_otp):
                if User.objects.filter(email=session_email).exists():
                    if new_password == confirm_new_password:
                        user = User.objects.get(email=session_email)
                        user.password = confirm_new_password
                        user.save()
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')

                if Team.objects.filter(email=session_email):
                    if new_password == confirm_new_password:
                        team = Team.objects.get(email=session_email)
                        team.password = confirm_new_password
                        team.save()
                        
                        del request.session['OTP'] 
                        del request.session['email']
                        messages.error(request,'Password reset completed sucessfully')
                        return redirect('forgot_password_2')
                    else:
                        messages.error(request,'Both Password Must be same')
                        return redirect('forgot_password_2')   
                else:
                    messages.error(request,'Please generate OTP first')
                    return redirect('forgot_password_2')
            else:
                messages.error(request,'Please enter correct otp')
                return redirect('forgot_password_2')
        else:
            messages.error(request,'Please generate OTP first')
            return redirect('forgot_password_2')
        
    else:
        return render(request,'forgot_password_2.html')




