# context_processors.py
from .models import *

def custom_user(request):
    user_id = request.session.get('current_user_id')
    if user_id:
        try:
            user = User.objects.get(user_id=user_id)
            return {'current_user': user}
        except User.DoesNotExist:
            pass
    return {'current_user': None}

def custom_subuser(request):
    subuser_id = request.session.get('current_subuser_id')
    if subuser_id:
        try:
            subuser = Team.objects.get(subuser_id=subuser_id)
            return {'current_subuser': subuser}
        except Team.DoesNotExist:
            pass
    return {'current_subuser': None}

def getAllCompanies(request):
    user_context = custom_user(request)
    current_user = user_context.get('current_user')

    subuser_context = custom_subuser(request)
    current_subuser = subuser_context.get('current_subuser')
    
    if current_user:
        current_user_companies = Company.objects.filter(user_id=current_user.user_id)
        return {'current_user_companies':current_user_companies}
    if current_subuser:
        current_user_companies = Company.objects.filter(company_id=current_subuser.company_id)
        return {'current_user_companies':current_user_companies}
    else:
        return {'current_user_companies':None}