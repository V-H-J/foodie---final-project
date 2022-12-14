# Generated by Django 4.0.6 on 2022-08-04 18:54

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
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.TextField(null=True)),
                ('city', models.TextField(null=True)),
                ('state', models.TextField(null=True)),
                ('zipcode', models.TextField(null=True)),
            ],
            options={
                'db_table': 'addresses',
            },
        ),
        migrations.CreateModel(
            name='BusinessExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_address', models.TextField(null=True)),
                ('business_city', models.TextField(null=True)),
                ('business_state', models.TextField(null=True)),
                ('business_zipcode', models.TextField(null=True)),
                ('legal_name', models.TextField(null=True)),
                ('approval_status', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'business_extra',
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.businessextra')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'carts',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.TextField(null=True)),
                ('item_price', models.FloatField(null=True)),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.businessextra')),
            ],
            options={
                'db_table': 'restaurant_menu',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_name', models.TextField(null=True)),
                ('offer_description', models.TextField(null=True)),
                ('discount', models.IntegerField(null=True)),
                ('promo_code', models.CharField(max_length=10, null=True)),
            ],
            options={
                'db_table': 'offers',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50, null=True)),
                ('offer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.offer')),
                ('restaurant_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.businessextra')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'orders',
            },
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardnumber', models.CharField(max_length=16, null=True)),
                ('cardname', models.TextField(null=True)),
                ('cardtype', models.CharField(max_length=50, null=True)),
                ('expires', models.CharField(max_length=5, null=True)),
                ('cvv', models.IntegerField()),
            ],
            options={
                'db_table': 'payment_methods',
            },
        ),
        migrations.CreateModel(
            name='UserExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=10)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('delivery', 'Delivery Person'), ('business', 'Business')], max_length=10)),
                ('is_admin', models.BooleanField(null=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_extra',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.menu')),
                ('order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.order')),
            ],
            options={
                'db_table': 'order_items',
            },
        ),
        migrations.CreateModel(
            name='DeliveryPersonExtra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssn', models.CharField(max_length=10, null=True)),
                ('legal_name', models.TextField(null=True)),
                ('approval_status', models.CharField(max_length=100, null=True)),
                ('user_extra_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.userextra')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'delivery_person_extra',
            },
        ),
        migrations.CreateModel(
            name='Default',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.address')),
                ('payment_method_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.paymentmethod')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'defaults',
            },
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.cart')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.menu')),
            ],
            options={
                'db_table': 'cart_items',
            },
        ),
        migrations.AddField(
            model_name='businessextra',
            name='user_extra_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodie.userextra'),
        ),
        migrations.AddField(
            model_name='businessextra',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
