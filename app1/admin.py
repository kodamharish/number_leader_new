from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username','user_type','company_type')
    list_display_links = ('user_id',)  
admin.site.register(User, UserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id','user_id','name')
    list_display_links = ('company_id',)  
admin.site.register(Company, CompanyAdmin)

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_id','sector')
    list_display_links = ('company_id',)  
admin.site.register(CompanyProfile, CompanyProfileAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('subuser_id','company_id','creator_id','username','user_type')
    list_display_links = ('company_id',)  
admin.site.register(Team, TeamAdmin)

class FounderAdmin(admin.ModelAdmin):
    list_display = ('company_id','id')
    list_display_links = ('company_id',)  
admin.site.register(Founder, FounderAdmin)

class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ('company_id','url')
    list_display_links = ('company_id',)  
admin.site.register(SocialMedia, SocialMediaAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('company_id','name')
    list_display_links = ('company_id',)  
admin.site.register(Client, ClientAdmin)



admin.site.register(HomogenousProduct)
admin.site.register(HeterogenousProduct)
admin.site.register(CompanyRevenue)

#later use
#admin.site.register(NewsOfIndustry)
#admin.site.register(NewsOfInvestment)
#admin.site.register(ProfitLossBalanceSheet)