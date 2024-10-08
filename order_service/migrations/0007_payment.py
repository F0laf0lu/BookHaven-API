# Generated by Django 4.2.14 on 2024-08-22 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('order_service', '0006_order_total_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('reference', models.CharField(max_length=100, unique=True)),
                ('access_code', models.CharField(max_length=100)),
                ('verified', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order_service.order')),
            ],
        ),
    ]
