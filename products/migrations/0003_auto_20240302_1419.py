# Generated by Django 5.0.2 on 2024-03-02 14:19

from django.db import migrations

def generate_unique_slug(apps, schema_editor):
    Product = apps.get_model('products', 'Product')
    for product in Product.objects.all():
        product.slug = "{}-{}".format(product.title, product.id)  # replace this with your own slug generation logic
        product.save()

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_category_product_created_at_and_more'),
    ]

    operations = [
        migrations.RunPython(generate_unique_slug),
    ]


    