from django.contrib import admin
from django.contrib import messages
from .models import Product, Category , Supplier, SupplierDetail, HomePage, Commande
from decimal import Decimal
from django.utils.html import format_html

from import_export.admin import ImportExportModelAdmin

class ProductAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('image_tag','name', 'price','supplier','category_list','stock_status','short_description' , 'quantity', 'formatted_created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    fields = ('name', 'price', 'description', 'quantity','categories','created_at','image','image_tag')
    readonly_fields = ('created_at','image_tag')
    list_per_page = 10
    list_editable = ('price', 'quantity')

    def formatted_created_at(self, obj):
        return obj.created_at.strftime('%d-%m-%Y %H:%M:%S')
    formatted_created_at.short_description = 'created_at'

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" style="border-radius:5px;" />'.format(obj.image.url))
        return "Pas d'image"

    image_tag.short_description = 'Aperçu'


    def short_description(self, obj):
        return obj.description[:40] + '...'
    short_description.short_description = 'Description'

    actions = ['set_price_to_zero', 'duplicate_products','apply_discount']

    def set_price_to_zero(self, request, queryset):
        queryset.update(price=0)
        self.message_user(request, "Prix mis à zéro pour les produits sélectionnés.")
    set_price_to_zero.short_description = "Mettre le prix à zéro"

    def duplicate_products(self, request, queryset):
        for product in queryset:
            product.pk = None
            product.save()
        self.message_user(request, "Produits dupliqués avec succès.")
    duplicate_products.short_description = "Dupliquer les produits sélectionnés"

    def apply_discount(self, request, queryset):
        discount_percentage = Decimal("0.9")  
        for product in queryset:
            if product.price:  
                new_price = Decimal(product.price) * discount_percentage  
                product.price = new_price  
                product.save()  
        self.message_user(request, f"Une remise de 10% a été appliquée.", messages.SUCCESS)
    apply_discount.short_description = "Appliquer une remise de 10 pourcent"

admin.site.register(Product, ProductAdmin)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'products_count','products_list')       
    search_fields = ['name']
    list_filter = ['name']
    ordering = ['name']
    fields = ['name']
    list_per_page = 10

    def products_count(self, obj):
        return obj.products.count()
    products_count.short_description = 'Nombre de produits'


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    fields = ('name', 'phone')
    list_display = ('name', 'phone')
    search_fields = ['name']


@admin.register(SupplierDetail)
class SupplierDetailAdmin(admin.ModelAdmin):
    list_display = ('supplier', 'address', 'contact_email', 'website', 'contact_person',)
    search_fields = ('contact_person',)
    list_filter = ('supplier',)
    fields = ('supplier', 'address', 'contact_email', 'website', 'contact_person', 'supplier_type', 
               'country', 'payment_terms', 'bank_account', 'region_served')
    list_per_page = 10


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ('site_name','logo_tag' ,'logo', 'welcome_titre', 
                    'formatted_welcome_message', 'action1_message', 'action1_lien', 
                    'action2_message', 'action2_lien', 'formatted_contact_message',
                    'formatted_about_message', 'formatted_footer_message', 'footer_bouton_message')
    
    fields = ('logo', 'site_name', 'welcome_titre', 'welcome_message', 'action1_message', 
              'action1_lien', 'action2_message', 'action2_lien', 'contact_message', 
              'about_message', 'footer_message', 'footer_bouton_message')
    readonly_fields = ('logo_tag',)
    
    def logo_tag(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="100px" style="border-radius:5px;" />'.format(obj.logo.url))
        return "Pas d'image"
    logo_tag.short_description = 'Logo'

    def formatted_welcome_message(self, obj):
        return format_html(obj.welcome_message)
    formatted_welcome_message.short_description = 'Message de bienvenue'

    def formatted_contact_message(self, obj):
        return format_html(obj.contact_message)
    formatted_contact_message.short_description = 'Message de contact'

    def formatted_about_message(self, obj):
        return format_html(obj.about_message)
    formatted_about_message.short_description = 'Message à propos'

    def formatted_footer_message(self, obj):
        return format_html(obj.footer_message)
    formatted_footer_message.short_description = 'Message du pied de page'

    def has_add_permission(self, request):
        if HomePage.objects.exists():
            return False
        return True
    

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'customer_name', 'status_colored', 'customer_email', 'customer_phone', 'created_at', 'payment', 'is_delivered')
    list_editable = ('is_delivered',)  
    search_fields = ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
    list_filter = ('customer_name', 'payment')
    fields = ('product', 'quantity', 'customer_name', 'customer_email', 'customer_phone', 'customer_address', 'payment')
    list_per_page = 5
 
    def status_colored(self, obj):
        """Affiche le statut avec une couleur : vert si livré, rouge sinon"""
        color = "green" if obj.is_delivered else "red"
        status = "Livrée" if obj.is_delivered else "En attente"
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', color, status)
 
    status_colored.short_description = 'Statut'

    def total_commande(self, obj):
        """Calcule le total de la commande"""
        return obj.quantity * obj.product.price if obj.product and obj.product.price else 0
 
    total_commande.short_description = 'Total (€)'

