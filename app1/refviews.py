from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request,'home.html')
def about(request):
    return render(request,'about.html')

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
        role = request.POST.get('role')


        
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
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('sign_up')
            
        if User.objects.filter(email=email).exists():
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
            role = role
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
        return render(request, 'sign_up.html')






# def investorSignUp(request):
#     if request.method == 'POST':
#         # Extract form data using request.POST.get
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname', '')  # Optional field
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         # Validate passwords
#         if password != confirm_password:
#             messages.error(request,'Passwords do not match')
#             return redirect('investor_sign_up')
            
#         # Validate if the username or email already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request,'Username already exists')
#             return redirect('investor_sign_up')
            
#         if User.objects.filter(email=email).exists():
#             messages.error(request,'Email already exists')
#             return redirect('investor_sign_up')         
#         # Create and save User object
#         user = User(
#             username=username,
#             email=email,
#             phone_number=phone_number,
#             linkedin_url=linkedin_url,
#             firstname=firstname,
#             lastname=lastname,
#             password=password,
#             role = 'investor'
#         ) 
#         user.save()
#         messages.error(request,'Data Submitted Sucessfully')
#         return redirect('investor_sign_up') 
           
#     else:
#         return render(request, 'investor_sign_up.html')
    

# def caFirmSignUp(request):
#     if request.method == 'POST':
#         # Extract form data using request.POST.get
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         phone_number = request.POST.get('phone_number')
#         linkedin_url = request.POST.get('linkedin_url', '')  # Optional field
#         firstname = request.POST.get('firstname')
#         lastname = request.POST.get('lastname', '')  # Optional field
#         password = request.POST.get('password')
#         confirm_password = request.POST.get('confirm_password')
        
#         # Validate passwords
#         if password != confirm_password:
#             messages.error(request,'Passwords do not match')
#             return redirect('ca_firm_sign_up')
            
#         # Validate if the username or email already exists
#         if User.objects.filter(username=username).exists():
#             messages.error(request,'Username already exists')
#             return redirect('ca_firm_sign_up')
            
#         if User.objects.filter(email=email).exists():
#             messages.error(request,'Email already exists')
#             return redirect('ca_firm_sign_up')         
#         # Create and save User object
#         user = User(
#             username=username,
#             email=email,
#             phone_number=phone_number,
#             linkedin_url=linkedin_url,
#             firstname=firstname,
#             lastname=lastname,
#             password=password,
#             role = 'CA firm'
#         ) 
#         user.save()
#         messages.error(request,'Data Submitted Sucessfully')
#         return redirect('ca_firm_sign_up') 
           
#     else:
#         return render(request, 'ca_firm_sign_up.html')

#Admin

from .context_processors import custom_user




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
        if User.objects.filter(username=username).exists():
            messages.error(request,'Username already exists')
            return redirect('add_team')
            
        if User.objects.filter(email=email).exists():
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
        messages.error(request,'User Created Successfully')
        return redirect('add_team')       
           
    else:
        return render(request, 'admin/add_team.html')
    
def updateTeam(request):
    pass

def myTeam(request):
    if request.method == 'POST':
        pass          
    else:
        search_query = request.GET.get('search', '')
    
        if search_query:
            total_team_data = Team.objects.filter(username__icontains=search_query)
        else:
            total_team_data = Team.objects.all()

        paginator = Paginator(total_team_data, 10)  # Show 10 team members per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        total_team_data = Team.objects.all()
        context = {'total_team_data':total_team_data}
        return render(request, 'admin/my_team.html',context)
    

def adminDashboard(request):
    return render(request,'admin/dashboard.html')

def myCompany(request):
    return render(request,'admin/my_company.html')

#Editor
def editorDashboard(request):
    return render(request,'editor/dashboard.html')
#User
def userDashboard(request):
    return render(request,'user/dashboard.html')