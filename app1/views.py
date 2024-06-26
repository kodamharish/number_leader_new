from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator
from .context_processors import custom_user,custom_subuser

#Mail Configuration
from django.core.mail import send_mail
from numberleader import settings
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

def sign_up_new(request):
    return render(request,'sign_up_new.html')


def login_new(request):
    return render(request,'login_new.html')
#Login and Logout
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
        
#         # Check if the user exists
#         if User.objects.filter(username=username).exists() and Team.objects.filter(username=username):
#             user = User.objects.get(username=username)
#             team = Team.objects.get(username=username)

#             # Check if the password is correct
#             if check_password(password, user.password or team.password):
#                 # Password is correct, proceed with login
#                 if user:
#                     request.session['current_user_id'] = user.user_id
#                 if team:
#                     request.session['current_user_id'] = team.subuser_id
#                 if user.user_type == 'admin':
#                     return redirect('admin_dashboard')
#                 elif team.user_type == 'editor':
#                     return redirect('editor_dashboard')
#                 elif team.user_type == 'user':
#                     return redirect('user_dashboard')
#             else:
#                 # Incorrect password
#                 messages.error(request, 'Invalid username or password')
#                 return render(request, 'login.html')
#         else:
#             # User does not exist
#             messages.error(request, 'Invalid username or password')
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user exists in both User and Team models
        user = User.objects.filter(username=username).first()
        team = Team.objects.filter(username=username).first()

        if user:
            if check_password(password, user.password):
                request.session['current_user_id'] = user.user_id
                if user.user_type == 'admin':
                    return redirect('admin_dashboard')
                if user.user_type == 'super_admin':
                    return redirect('super_admin_dashboard')
                # elif user.user_type == 'editor':
                #     return redirect('editor_dashboard')
                # elif user.user_type == 'user':
                #     return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
        elif team:
            if check_password(password, team.password):
                request.session['current_subuser_id'] = team.subuser_id
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

# Start Up
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
        founder_name = request.POST.get('founder_name')
        founder_email = request.POST.get('founder_email')
        founder_linkedin_url = request.POST.get('founder_linkedin_url')
        founder_phone_number = request.POST.get('founder_phone_number')
        
        # Validate passwords
        if password != confirm_password:
            messages.error(request,'Passwords do not match')
            return redirect('sign_up')
            
        # Validate if the username or email already exists
        if User.objects.filter(username=username).exists() or Team.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('sign_up')
            
        if User.objects.filter(email=email).exists() or Team.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('sign_up')
            
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
                company_name=company_name,
                company_email=company_email,
                company_website_url=company_website_url,
                company_linkedin_url=company_linkedin_url,
                founder_name=founder_name,
                founder_email=founder_email,
                founder_linkedin_url=founder_linkedin_url,
                founder_phone_number=founder_phone_number,
                subscription_type = subscription_type
                
            )
            
            company.save()

            # Ensure the company was saved correctly
            if company.pk:
                messages.error(request,'User Created Succesfully')
                return redirect('sign_up')
                
            else:
                messages.error(request,'Something went wrong please try again later')
                return redirect('sign_up')
                
        else:
            messages.error(request,'Something went wrong please try again later')
            return redirect('sign_up')
           
    else:
        return render(request, 'sign_up_new.html')





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
        total_team_data = Team.objects.filter(creator_id =current_user)
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

        # Fetch the User instance for the creator_id
        creator_user = User.objects.get(user_id=current_user.user_id)
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
        message=txt.format(firstname,lastname,email,username,password,phone_number,linkedin_url,user_type,company_id.company_name,signin_url)
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

        # Fetch the User instance for the creator_id
        creator_user = User.objects.get(user_id=current_user.user_id)
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

def addCompany(request):
    if request.method == 'POST':
        # Company Details
        user_id = request.POST.get('user_id')
        company_name = request.POST.get('company_name')
        company_email = request.POST.get('company_email')
        company_website_url = request.POST.get('company_website_url')
        company_linkedin_url = request.POST.get('company_linkedin_url')
        subscription_type = request.POST.get('subscription_type') 
        # Founders Details
        founder_name = request.POST.get('founder_name')
        founder_email = request.POST.get('founder_email')
        founder_linkedin_url = request.POST.get('founder_linkedin_url')
        founder_phone_number = request.POST.get('founder_phone_number')
        user_context = custom_user(request)
        current_user = user_context.get('current_user')  

        # Company profile
        excecutive_summary = request.POST.get('excecutive_summary')
        technology_profile = request.POST.get('technology_profile')
        type_of_industry = request.POST.get('type_of_industry')
        no_of_employees = request.POST.get('no_of_employees')
        ceo = request.POST.get('ceo')
        cfo = request.POST.get('cfo')
        cmo = request.POST.get('cmo')
        vp = request.POST.get('vp')

        # Products
        product_name = request.POST.get('product_name')

        # Fetch the User instance for the creator_id
        #creator_user = User.objects.get(user_id=current_user.user_id)

        # Create the Company instance
        company = Company(
                user_id=current_user,  # This should match the foreign key field in Company model
                company_name=company_name,
                company_email=company_email,
                company_website_url=company_website_url,
                company_linkedin_url=company_linkedin_url,
                subscription_type=subscription_type,
                founder_name=founder_name,
                founder_email=founder_email,
                founder_linkedin_url=founder_linkedin_url,
                founder_phone_number=founder_phone_number,
            )
        company.save()

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

        products = Product(
            company_id=company,
            product_name = product_name
        )
        products.save()
        messages.success(request, 'Data saved Successfully')
        return redirect('add_company')
    else:
        return render(request, 'admin/add_company.html')



def updateCompany(request, company_id):
    if request.method == 'POST':
        # Fetch existing company and profile
        company = get_object_or_404(Company, company_id=company_id)
        company_profile = get_object_or_404(CompanyProfile, company_id=company_id)
        products = get_object_or_404(Product, company_id=company_id)

        
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

        # Products
        products.product_name = request.POST.get('product_name')
        
        # Save the updates
        company.save()
        company_profile.save()
        products.save()

        messages.success(request, 'Data updated successfully')
        return redirect('update_company', company_id=company_id)
    else:
        # Fetch existing company and profile for initial form rendering
        company = get_object_or_404(Company, company_id=company_id)
        company_profile = get_object_or_404(CompanyProfile, company_id=company_id)
        products = get_object_or_404(Product, company_id=company_id)

        
        context = {
            'company': company,
            'company_profile': company_profile,
            'products':products
        }
        
        return render(request, 'admin/update_company.html', context)



# def companyProfile(request, id):
#     #company = get_object_or_404(Company, company_id=id)
#     #company_profile = get_object_or_404(CompanyProfile, company_id=id)
#     company = Company.objects.get(company_id=id)
#     company_profile = CompanyProfile.objects.get(company_id=id)

#     if company:
#         if company_profile:
#             products = Product.objects.filter(company_id=id) 
#         else:
#             company_profile = None
    
#     context = {
#         'company': company,
#         'company_profile': company_profile,
#         'Products':products
#     }
#     return render(request, 'admin/company_profile.html',context)

# def companyProfile(request, id):
#     company = get_object_or_404(Company, company_id=id)
#     try:
#             company_profile = CompanyProfile.objects.get(company_id=id)
#             products = Product.objects.get(company_id=id)

#     except CompanyProfile.DoesNotExist or Product.DoesNotExist:
#             company_profile = None
#             products = None

#     if request.method == 'POST':
#         # Company profile
#         company_profile.excecutive_summary = request.POST.get('excecutive_summary')
#         company_profile.technology_profile = request.POST.get('technology_profile')
#         company_profile.type_of_industry = request.POST.get('type_of_industry')
#         company_profile.no_of_employees = request.POST.get('no_of_employees')
#         company_profile.ceo = request.POST.get('ceo')
#         company_profile.cfo = request.POST.get('cfo')
#         company_profile.cmo = request.POST.get('cmo')
#         company_profile.vp = request.POST.get('vp')

#         # Products
#         products.product_name = request.POST.get('product_name')
#     else:
#         print(products)
#         context = {
#             'company': company,
#             'company_profile': company_profile,
#             'products': products
#         }

#         return render(request, 'admin/company_profile.html', context)

def companyProfile(request, id):
    company = get_object_or_404(Company, company_id=id)
    try:
        company_profile = CompanyProfile.objects.get(company_id=id)
    except CompanyProfile.DoesNotExist:
        company_profile = None

    try:
        products = Product.objects.filter(company_id=id)
    except Product.DoesNotExist:
        products = None

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

            # Products
            product_name = request.POST.get('product_name')
            products = Product(
                company_id=company,
                product_name = product_name
            )
            products.save()
            messages.success(request, 'Data saved Successfully')
            return redirect('comprehensive_profile')
    else:
        context ={'company': company,'company_profile': company_profile,'products': products
        }
        return render(request, 'admin/company_profile.html', context)

def comprehensiveProfile(request):
    company_profile = CompanyProfile.objects.first()
    products = Product.objects.all()
    context ={'company_profile': company_profile, 'products': products}
    return render(request, 'admin/comprehensive.html', context)

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




