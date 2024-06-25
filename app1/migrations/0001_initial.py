# Generated by Django 5.0.6 on 2024-06-25 06:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('company_name', models.CharField(max_length=100, null=True)),
                ('company_email', models.EmailField(max_length=254, null=True)),
                ('company_website_url', models.URLField(null=True)),
                ('company_linkedin_url', models.URLField(null=True)),
                ('subscription_type', models.CharField(max_length=20, null=True)),
                ('founder_name', models.CharField(max_length=100, null=True)),
                ('founder_email', models.EmailField(max_length=254, null=True)),
                ('founder_linkedin_url', models.URLField(null=True)),
                ('founder_phone_number', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyIDSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='NewsOfIndustry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='NewsOfInvestment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SubUserIDSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(editable=False, max_length=10, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('linkedin_url', models.URLField(null=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=10)),
                ('user_type', models.CharField(default='admin', max_length=12)),
                ('company_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UserIDSequence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_id', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excecutive_summary', models.TextField()),
                ('technology_profile', models.TextField(null=True)),
                ('type_of_industry', models.CharField(max_length=50)),
                ('no_of_employees', models.IntegerField()),
                ('ceo', models.CharField(max_length=100)),
                ('cfo', models.CharField(max_length=100)),
                ('cmo', models.CharField(max_length=100)),
                ('vp', models.CharField(max_length=100)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.company')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=250, null=True)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.company')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('subuser_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.IntegerField()),
                ('linkedin_url', models.URLField(null=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50, null=True)),
                ('password', models.CharField(max_length=10)),
                ('user_type', models.CharField(max_length=12)),
                ('company_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.company')),
                ('creator_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user')),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.user'),
        ),
    ]
