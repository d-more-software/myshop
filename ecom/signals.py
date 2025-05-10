from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Commande
 
@receiver(post_save, sender=Commande)
def update_product_quantity(sender, instance, created, **kwargs):
    """
    Décrémente la quantité du produit après validation de la commande.
    """
    if created:  
        if instance.product.quantity >= instance.quantity:
            instance.product.quantity -= instance.quantity
            instance.product.save()
        else:
            print(f"Stock insuffisant pour le produit {instance.product.name}. Quantité disponible: {instance.product.quantity}")