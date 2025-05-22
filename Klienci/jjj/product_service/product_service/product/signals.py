from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal, ROUND_UP, ROUND_HALF_UP
from django.utils.text import slugify
from .models import Product

VAT_RATE = Decimal('0.23')
MARKUP_RATE = Decimal('0.20')


@receiver(pre_save, sender=Product)
def wylicz_cene(sender, instance, **kwargs):
    if instance.price_net_no_markup:
        instance.price_gross_no_markup = (instance.price_net_no_markup * (1 + VAT_RATE)).quantize(Decimal('0.01'),
                                                                                                  rounding=ROUND_HALF_UP)
        instance.price_net_with_markup = (instance.price_net_no_markup * (1 + MARKUP_RATE)).quantize(Decimal('0.01'),
                                                                                                     rounding=ROUND_HALF_UP)
        instance.price_gross_with_markup = (instance.price_net_with_markup * (1 + VAT_RATE)).quantize(Decimal('0.01'),
                                                                                                      rounding=ROUND_HALF_UP)

@receiver(pre_save)
def ustaw_slug(sender, instance, **kwargs):
    if hasattr(instance, 'slug') and not instance.slug:
        instance.slug = slugify(instance.name)
        base_slug = slugify(instance.name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
            instance.slug = slug