from enum import unique

from django.db import models

from pesanile_accounting.models import AssetType, AccountCategory, AccountType, GLLine
import random


def generate_custom_id(prefix=None):
    print('prefix ', prefix)
    if prefix is not None:
        return str(str(prefix) + '-' + str(random.randint(1111, 9999)))
    else:
        return str('NA' + '-' + str(random.randint(1111, 9999)))


# Create your models here.
class CategoryType(models.Model):
    type_code = models.CharField(max_length=10, primary_key=True, editable=False, verbose_name = 'Code Of Category Type')
    type_name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.type_code:
            self.type_code = generate_custom_id('TC')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.type_name)

class Category(models.Model):
    code = models.CharField(max_length=10, primary_key=True, editable=False, verbose_name = 'Code Of Category')
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name = 'type_of_category', null=True)
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_custom_id('CC')
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.category_name)

class DefaultAccountSetUp(models.Model):
    code = models.CharField(max_length=50, primary_key=True, editable=False, verbose_name = "Default Account Set Up Code")
    category_type = models.ForeignKey(CategoryType, null=True, on_delete = models.CASCADE, related_name="das_category_type", verbose_name= "Category Type")
    category_name = models.ForeignKey(Category, null=True, on_delete = models.CASCADE, related_name="das_category_name", verbose_name= "Category Name")
    # assets_type = models.ForeignKey(AssetType, on_delete = models.CASCADE, related_name = "das_asset_type", verbose_name = "Name Of Assets Types")
    account_type = models.ForeignKey(AccountType, on_delete = models.CASCADE, related_name = "das_account_type", verbose_name = "Name Of Account Type")
    account_category = models.ForeignKey(AccountCategory, on_delete = models.CASCADE, related_name = "das_account_category", verbose_name = "Name Of Account Category")
    glline = models.ForeignKey(GLLine, on_delete = models.CASCADE, related_name="das_glline", verbose_name= "Name Of Gl Line")


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_custom_id('DASC')
        super().save(*args, **kwargs)
