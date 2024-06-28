# from django.shortcuts import redirect
# from django.urls import reverse
# from django.utils.deprecation import MiddlewareMixin

# class SessionExpiryMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         login_url = reverse('login')  # Get the URL for the login page
#         if not request.session.get('current_user_id') and not request.session.get('current_subuser_id'):
#             # User is not authenticated if neither session variable is set
#             if request.path != login_url and request.path != reverse('sign_up') and not request.path.startswith('/admin/'):
#                 # Exclude login, signup, and admin paths if needed
#                 return redirect(login_url)  # Redirect to the login page


from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

class SessionExpiryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        login_url = reverse('login')  # Get the URL for the login page
        signup_url = reverse('signup')  # Get the URL for the signup page
        home_url = reverse('home')  # Get the URL for the home page
        about_url = reverse('about')  # Get the URL for the about page
        root_url = reverse('home')  # Assuming '' path maps to home

        # Define a list of paths to exclude from session check
        excluded_paths = [login_url, signup_url, home_url, about_url, root_url]
        
        if not request.session.get('current_user_id') and not request.session.get('current_subuser_id'):
            # User is not authenticated if neither session variable is set
            if request.path not in excluded_paths and not request.path.startswith('/admin/'):
                # Exclude login, signup, home, about, and admin paths if needed
                return redirect(login_url)  # Redirect to the login page
