# Generated by Django 5.2 on 2025-05-01 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom', '0008_product_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=255)),
                ('logo', models.ImageField(upload_to='./')),
                ('welcome_titre', models.CharField(max_length=255)),
                ('welcome_message', models.TextField()),
                ('action1_message', models.CharField(max_length=255)),
                ('action1_lien', models.CharField(max_length=255)),
                ('action2_message', models.CharField(max_length=255)),
                ('action2_lien', models.CharField(max_length=255)),
                ('contact_message', models.TextField()),
                ('about_message', models.TextField()),
                ('footer_message', models.TextField()),
                ('footer_bouton_message', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': "Page d'accueil",
                'verbose_name_plural': "Pages d'accueil",
            },
        ),
    ]
