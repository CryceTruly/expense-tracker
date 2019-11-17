# Generated by Django 2.2.6 on 2019-11-17 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255)),
                ('spent_on', models.DateField()),
                ('description', models.TextField(blank=True)),
                ('amount', models.FloatField()),
                ('currency', models.CharField(default='Ugx', max_length=20)),
                ('category', models.CharField(choices=[('ONLINE_SERVICES', 'ONLINE_SERVICES'), ('RENT', 'RENT'), ('BUSINESS_MISCELLENOUS', 'BUSINESS_MISCELLENOUS'), ('TRAVEL', 'TRAVEL'), ('GENERAL_MERCHANDISE', 'GENERAL_MERCHANDISE'), ('RESTUARANTS', 'RESTUARANTS'), ('ENTERTAINMENT', 'ENTERTAINMENT'), ('GASOLINE_FUEL', 'GASOLINE_FUEL'), ('INSURANCE', 'INSURANCE'), ('OTHERS', 'OTHERS')], max_length=200)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-spent_on'],
            },
        ),
    ]
