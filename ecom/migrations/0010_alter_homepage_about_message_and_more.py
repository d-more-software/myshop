# Generated by Django 5.2 on 2025-05-01 17:46

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0009_homepage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='about_message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='contact_message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='footer_message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='homepage',
            name='welcome_message',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('customer_name', models.CharField(max_length=255)),
                ('customer_email', models.EmailField(max_length=254)),
                ('customer_phone', models.CharField(max_length=20)),
                ('customer_address', models.TextField()),
                ('payment', models.CharField(choices=[('livraison', 'Paiement à la livraison')], max_length=50)),
                ('is_delivered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecom.product')),
            ],
            options={
                'verbose_name': 'Commande',
                'verbose_name_plural': 'Commandes',
            },
        ),
    ]
