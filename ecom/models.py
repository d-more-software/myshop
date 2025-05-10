from django.db import models
from django.core.validators import MinValueValidator
from ckeditor.fields import RichTextField


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', related_name='products', blank=True)
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, related_name='products', blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def category_list(self):  
        cats = self.categories.all()
        if not cats:
            return "Aucune catégorie"
        else:
            return ", ".join([category.name for category in cats])
    category_list.fget.short_description = "Categories"

    @property
    def stock_status(self):
        if self.quantity > 0:
            return "En stock"
        else:
            return "Rupture de stock"
    stock_status.fget.short_description = "stock"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Categorie"

    @property
    def products_list(self):
        products = self.products.all()
        if not products.exists():  
            return "Aucun produit"
        else:
            return ", ".join([product.name for product in products])
    products_list.fget.short_description = "Produits"

    @property
    def products_count(self):
        return self.products.count()
    products_count.fget.short_description = "Nombre de produits"
    products_count.fget.admin_order_field = 'products_count'


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fournisseur'


class SupplierDetail(models.Model):
    supplier = models.OneToOneField(Supplier, on_delete=models.SET_NULL, null=True, blank=True, related_name='details')
    address = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    supplier_type = models.CharField(
        max_length=50, 
        choices=[('distributeur', 'Distributeur'), ('fabricant', 'Fabricant'), ('revendeur', 'Revendeur')],
        blank=True, 
        null=True
    )
    country = models.CharField(max_length=100, blank=True, null=True)
    payment_terms = models.CharField(max_length=100, blank=True, null=True)
    bank_account = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    region_served = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Details of {self.supplier.name}"

    class Meta:
        verbose_name = 'Détail Fournisseur'
        verbose_name_plural = 'Détails Fournisseurs'


class HomePage(models.Model):
    site_name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='./')
    welcome_titre = models.CharField(max_length=255)
    welcome_message = RichTextField()
    action1_message = models.CharField(max_length=255)
    action1_lien = models.CharField(max_length=255)
    action2_message = models.CharField(max_length=255)
    action2_lien = models.CharField(max_length=255)
    contact_message = RichTextField()
    about_message = RichTextField()
    footer_message = RichTextField()
    footer_bouton_message = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Page d\'accueil'
        verbose_name_plural = 'Pages d\'accueil'

    def __str__(self):
        return "Page d'accueil"


class Commande(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=255)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    payment = models.CharField(max_length=50, choices=[('livraison', 'Paiement à la livraison')])
    is_delivered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande {self.id} - {self.customer_name}"

    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)