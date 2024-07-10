from django.db import models
from django.contrib.auth.hashers import make_password


# Create your models here.
class UserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class CompanyIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)
    
class SubUserIDSequence(models.Model):
    current_id = models.IntegerField(default=0)
    def __str__(self):
        return str(self.current_id)

class User(models.Model):
    user_id = models.CharField(max_length=10, primary_key=True, editable=False)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=False)
    linkedin_url = models.URLField(null=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=150,null=False)  
    user_type = models.CharField(max_length=12,default='admin')
    company_type = models.CharField(max_length=20)
    
     

    def save(self, *args, **kwargs):
        if not self.user_id:
            user_sequence, created = UserIDSequence.objects.get_or_create(pk=1)
            user_sequence.current_id += 1
            self.user_id = f'NL{user_sequence.current_id:03d}'
            user_sequence.save()
        if self.password:
            # Hash the password
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    def __str__(self):
        return self.user_id
    
class Company(models.Model):
    # Company Details
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    company_id = models.CharField(max_length=10,primary_key=True , editable=False)
    name = models.CharField(max_length=100,null=True)
    email = models.EmailField(null=True)
    website_url = models.URLField(null=True)
    linkedin_url = models.URLField(null=True)
    subscription_type = models.CharField(max_length=20,null=True)

    def save(self, *args, **kwargs):
        if not self.company_id:
            company_sequence, created = CompanyIDSequence.objects.get_or_create(pk=1)
            company_sequence.current_id += 1
            self.company_id = f'C{company_sequence.current_id:03d}'
            company_sequence.save()
        super(Company, self).save(*args, **kwargs)
    def __str__(self):
        return self.company_id

class CompanyProfile(models.Model):
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    excecutive_summary = models.TextField(null=True)
    technology_profile=models.TextField(null=True)
    sector = models.CharField(max_length=50)
    no_of_employees = models.IntegerField(null=True)
    business_introductory_video_file = models.FileField(upload_to='business_introductory',null=True)
    business_introductory_video_url = models.URLField(null=True)
    business_plan = models.FileField(upload_to='business_plan',null=True)
    vision=models.TextField()
    mission=models.TextField()
    usp=models.TextField()
    date_of_incorporation = models.DateField(null= True)
    # def __str__(self):
    #     return self.company_id

class Founder(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='founders')
    name=models.CharField(max_length=50)
    linkedin_url=models.URLField()
    short_profile=models.TextField(null=True)
    photo=models.ImageField(upload_to='photos',null=True)
    phone_number=models.IntegerField()
    email=models.EmailField()

class SocialMedia(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE,related_name='social_media')
    #name=models.CharField(max_length=25)
    url=models.URLField()

class Client(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='clients')
    name=models.CharField(max_length=25)
    logo=models.ImageField(upload_to='clients_logo',null=True)

class CapTable(models.Model):
    company_id=models.ForeignKey(Company, on_delete=models.CASCADE,related_name='cap_table')
    name = models.CharField(max_length=200)
    email= models.EmailField()
    linkedin_url=models.URLField()
    photo = models.ImageField(upload_to='photos',null=True)
    percentage_of_shares= models.DecimalField(max_digits=5,decimal_places=2)







class Team(models.Model):
    subuser_id = models.CharField(max_length=10, primary_key=True)
    #creator_id = models.ForeignKey(User,on_delete=models.CASCADE)
    creator_id = models.CharField(max_length=15)
    company_id = models.ForeignKey(Company,on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(null=False)
    phone_number = models.IntegerField(null=False)
    linkedin_url = models.URLField(null=True)
    firstname = models.CharField(max_length=50,null=False)
    lastname = models.CharField(max_length=50,null=True)
    password = models.CharField(max_length=10,null=False)  
    user_type = models.CharField(max_length=12)

    def save(self, *args, **kwargs):
        if not self.subuser_id:
            subuser_sequence, created = SubUserIDSequence.objects.get_or_create(pk=1)
            subuser_sequence.current_id += 1
            self.subuser_id = f'SUBNL{subuser_sequence.current_id:03d}'
            subuser_sequence.save()
        if self.password:
            # Hash the password
            self.password = make_password(self.password)
        super(Team, self).save(*args, **kwargs)
    def __str__(self):
        return self.subuser_id




class HomogenousProduct(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    selling_price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    units_sold = models.IntegerField()
    expected_growth_rate = models.IntegerField()
    revenue_from_product = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def calculate_revenue_from_product(self):
        if isinstance(self.selling_price_per_unit, str):
            self.selling_price_per_unit = float(self.selling_price_per_unit)
        if isinstance(self.units_sold, str):
            self.units_sold = int(self.units_sold)
        return self.selling_price_per_unit * self.units_sold

    def save(self, *args, **kwargs):
        # Calculate revenue_from_product before saving
        self.revenue_from_product = self.calculate_revenue_from_product()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


 
class HeterogenousProduct(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    expected_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    expected_growth_rate = models.IntegerField()
    def __str__(self):
        return self.product_name
    
class CompanyRevenue(models.Model):
    company_id = models.ForeignKey(Company, on_delete=models.CASCADE)
    total_revenue = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)

    def calculate_total_revenue(self):
        homogenous_revenue = HomogenousProduct.objects.filter(company_id=self.company_id).aggregate(total=models.Sum('revenue_from_product'))['total'] or 0
        heterogenous_revenue = HeterogenousProduct.objects.filter(company_id=self.company_id).aggregate(total=models.Sum('expected_revenue'))['total'] or 0
        return homogenous_revenue + heterogenous_revenue
    
    def save(self, *args, **kwargs):
        # Calculate total_revenue before saving
        self.total_revenue = self.calculate_total_revenue()
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"Total Revenue for {self.company_id}"







# later use

class NewsOfIndustry(models.Model):
    pass
class NewsOfInvestment(models.Model):
    pass

#Profit Loss Balance Sheet
class ProfitLossBalanceSheet(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    #income
    revenue_recurring = models.FloatField()
    revenue_one_time = models.FloatField()
    other_income = models.FloatField()
    total_income = models.FloatField()
    #expenses
    cost_of_materials_consumed = models.FloatField()
    changes_inventories_of_fg_wip = models.FloatField()
    emp_benefits_expenses = models.FloatField()
    depreciation_amortization_expenses = models.FloatField()
    finance_cost = models.FloatField()
    other_expenses = models.FloatField()
    total_expenses = models.FloatField()
    #tax
    profit_before_tax = models.FloatField()
    current_tax_expense = models.FloatField()
    deferred_tax = models.FloatField()
    profit_after_tax = models.FloatField()
