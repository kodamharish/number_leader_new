from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id','username','user_type','company_type')
    list_display_links = ('user_id',)  
admin.site.register(User, UserAdmin)

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_id','user_id','company_name')
    list_display_links = ('company_id',)  
admin.site.register(Company, CompanyAdmin)

class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = ('company_id','ceo')
    list_display_links = ('company_id',)  
admin.site.register(CompanyProfile, CompanyProfileAdmin)

# class ProductsAdmin(admin.ModelAdmin):
#     list_display = ('company_id','product_name')
#     list_display_links = ('company_id',)  
# admin.site.register(Product, ProductsAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('subuser_id','company_id','creator_id','username','user_type')
    list_display_links = ('company_id',)  
admin.site.register(Team, TeamAdmin)

admin.site.register(NewsOfIndustry)
admin.site.register(NewsOfInvestment)

