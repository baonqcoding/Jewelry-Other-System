"""Seed demo user/category/product for CodeceptJS UI tests."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.models import Category, Product


class Command(BaseCommand):
    help = "Seed E2E fixture data (user e2e_user + sample product)"

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username="e2e_user",
            defaults={
                "email": "e2e@example.com",
                "first_name": "E2E",
                "last_name": "Tester",
            },
        )
        user.set_password("Passw0rd!23")
        user.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"user e2e_user {'created' if created else 'updated'} (password Passw0rd!23)"
            )
        )

        category, _ = Category.objects.get_or_create(
            slug="nhan-bac",
            defaults={"name": "Nhan Bac", "is_sub": False},
        )
        product, created_p = Product.objects.get_or_create(
            name="Nhan Bac Test",
            defaults={
                "price": 150000,
                "detail": "San pham dung cho CodeceptJS E2E",
            },
        )
        if created_p or not product.category.filter(id=category.id).exists():
            product.category.add(category)
            product.price = 150000
            product.detail = product.detail or "San pham dung cho CodeceptJS E2E"
            product.save()

        self.stdout.write(
            self.style.SUCCESS(
                f"category={category.slug} product_id={product.id} name={product.name}"
            )
        )
