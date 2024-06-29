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
    password = models.CharField(max_length=10,null=False)  
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
    company_name = models.CharField(max_length=100,null=True)
    company_email = models.EmailField(null=True)
    company_website_url = models.URLField(null=True)
    company_linkedin_url = models.URLField(null=True)
    subscription_type = models.CharField(max_length=20,null=True)
    # Founders Details
    founder_name = models.CharField(max_length=100,null=True)
    founder_email = models.EmailField(null=True)
    founder_linkedin_url = models.URLField(null=True)
    founder_phone_number = models.IntegerField(null=True)
    
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
    excecutive_summary = models.TextField()
    technology_profile=models.TextField(null=True)
    type_of_industry = models.CharField(max_length=50)
    no_of_employees = models.IntegerField()
    ceo = models.CharField(max_length=100)
    cfo = models.CharField(max_length=100)
    cmo = models.CharField(max_length=100)
    vp = models.CharField(max_length=100)

class Product(models.Model):
    company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=250, null=True)

class NewsOfIndustry(models.Model):
    pass
class NewsOfInvestment(models.Model):
    pass



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





    