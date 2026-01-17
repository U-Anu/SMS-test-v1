from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from django.utils.timezone import now


class User(AbstractUser):
    first_name = models.CharField(max_length=30)
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30)
    dob = models.DateField(blank=False, null=True)
    phone_number = models.PositiveBigIntegerField(blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.username

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='company_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='company_updated_by')
    def __str__(self):
        return self.name

class Branch(models.Model):
    company = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='branches')
    name = models.CharField(max_length=255)
    branch_code = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    manager_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='branch_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='branch_updated_by')
    def __str__(self):
        return f"{self.name} - {self.company.name}"


class ItemCategory(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='categories') 
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class ItemSubCategory(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='subcategories') 
    category = models.ForeignKey(
        ItemCategory,
        on_delete=models.CASCADE,
        related_name='subcategories'
    )
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.category.name})"

class ItemMaster(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='items') 
    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        ItemSubCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )
    supplier = models.ForeignKey(
        'Supplier',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.name} ({self.item_code})"

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Liter", "Kilogram", "Piece"
    abbreviation = models.CharField(max_length=10, unique=True)  # e.g., "L", "kg", "pcs"

    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class ItemUnit(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="units")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)  # e.g., "Milliliter", "Gram"
    conversion_factor_to_base = models.DecimalField(max_digits=10, decimal_places=4)  # e.g., 1 Liter = 1000 Milliliters

    class Meta:
        unique_together = ("item", "unit")  # Prevent duplicate item-unit combinations

    def __str__(self):
        return f"{self.item.name} - {self.unit.name}"
    
class PriceStructure(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="price_structures")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)  # Unit for this price (e.g., "Liter", "Piece")
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit

    class Meta:
        unique_together = ("item", "unit", "effective_date")  # Prevent duplicate price entries for the same date

    def __str__(self):
        return f"{self.item.name} - {self.unit.name}: {self.price_per_unit}"

class Pack(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="packs")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)  # e.g., "Liter", "Piece"
    quantity = models.PositiveIntegerField()  # Number of units in the pack
    pack_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price for the pack

    class Meta:
        unique_together = ("item", "unit", "quantity", "effective_date")  # Prevent duplicate pack definitions

    def __str__(self):
        return f"{self.item.name} - {self.quantity} {self.unit.name} pack: {self.pack_price}"
        


class Supplier(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='vendors')  
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    services_or_products = models.TextField(null=True, blank=True)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
        ],
        default='active',
    )
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vendor_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='vendor_updated_by')

    def __str__(self):
        return self.name

class Store(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='stores')
    name = models.CharField(max_length=255, unique=True)
    location = models.TextField()
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    manager_name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    supplier_access = models.BooleanField(default=False)
    sales_access = models.BooleanField(default=False)
    transfer_access = models.BooleanField(default=False)
    return_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='store_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='store_updated_by')

    def __str__(self):
        return self.name


class SupplierStoreMapping(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='vendor_store_mappings') 
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name='store_mappings'
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='vendor_mappings'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vendor_store_mapping_created_by'
    )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='vendor_store_mapping_updated_by'
    )

    class Meta:
        unique_together = ('vendor', 'store')

    def __str__(self):
        return f"{self.supplier.name} - {self.store.name}"

class PackNameMaster(models.Model):
    pack_name = models.CharField(max_length=100, unique=True, help_text="Name of the pack (e.g., Box, Bundle)")
    pack_size = models.PositiveIntegerField(help_text="Number of pieces in the pack")
    description = models.TextField(null=True, blank=True, help_text="Additional details about the pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pack_name} ({self.pack_size} pieces)"

class ItemPackSize(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='pack_sizes')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='item_pack_sizes')
    pack_name = models.ForeignKey(
        'PackNameMaster',
        on_delete=models.CASCADE,
        related_name='item_pack_sizes',
        help_text="Reference to the Pack Name Master"
    )
    quantity_per_pack = models.PositiveIntegerField(help_text="Number of pieces per pack")
    price_per_pack = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for the entire pack")
    price_per_piece = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, help_text="Optional price for a single piece"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.pack_name.pack_name} ({self.quantity_per_pack} pcs)"

    class Meta:
        unique_together = ('item', 'supplier', 'pack_name')


class MainStoreToSupplierRequest(models.Model):
    RETURN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    store = models.ForeignKey(Store, related_name='supplier_returns', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='returns', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=RETURN_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Request from {self.store} to {self.supplier}"
    
class SubStoreToSupplierRequest(models.Model):
    main_request = models.ForeignKey(
        MainStoreToSupplierRequest, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='sub_requests')
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")
    unit_price = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='sub_requests')

    def __str__(self):
        return f"{self.quantity} of {self.item} for Request ID {self.main_request.id}"    

class MainStoreToSupplierReceive(models.Model):
    RETURN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    store = models.ForeignKey(
        Store, 
        related_name='supplier_returns_received', 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50, 
        choices=RETURN_STATUS_CHOICES, 
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Received by {self.store}"
    
class SubStoreToSupplierReceive(models.Model):
    main_receive = models.ForeignKey(
        MainStoreToSupplierReceive, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        ItemMaster, 
        on_delete=models.CASCADE, 
        related_name='received_items'
    )
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")
    unit_price = models.ForeignKey(
        Pack, 
        on_delete=models.CASCADE, 
        related_name='received_items'
    )

    def __str__(self):
        return f"{self.quantity} of {self.item} for Receive ID {self.main_receive.id}"    




class MainStoreToStoreRequest(models.Model):
    RETURN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    sending_store = models.ForeignKey(
        Store, 
        related_name='store_requests_sent', 
        on_delete=models.CASCADE
    )
    receiving_store = models.ForeignKey(
        Store, 
        related_name='store_requests_received', 
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50, 
        choices=RETURN_STATUS_CHOICES, 
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request from {self.sending_store} to {self.receiving_store}"
    
class SubStoreToStoreRequest(models.Model):
    main_request = models.ForeignKey(
        MainStoreToStoreRequest, 
        related_name='items', 
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        ItemMaster, 
        on_delete=models.CASCADE, 
        related_name='store_to_store_items'
    )
    unit_price = models.ForeignKey(
        Pack, 
        on_delete=models.CASCADE, 
        related_name='store_to_store_items'
    )

    def __str__(self):
        return f"{self.item} for Request ID {self.main_request.id}"    

class MainStoreToStoreReceive(models.Model):
    RETURN_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Received', 'Received'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    ]

    receiving_store = models.ForeignKey(
        Store,
        related_name='receives_initiated',
        on_delete=models.CASCADE
    )
    sending_store = models.ForeignKey(
        Store,
        related_name='receives_sent',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=50,
        choices=RETURN_STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Receive Record: {self.receiving_store} from {self.sending_store}"
    
class SubStoreToStoreReceive(models.Model):
    main_receive = models.ForeignKey(
        MainStoreToStoreReceive,
        related_name='items',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        ItemMaster,
        on_delete=models.CASCADE,
        related_name='store_to_store_received_items'
    )
    quantity = models.PositiveIntegerField(help_text="Quantity received")
    unit_price = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        related_name='store_to_store_received_items'
    )

    def __str__(self):
        return f"{self.quantity} of {self.item} for Receive ID {self.main_receive.id}"     


class StoreToSupplierReturn(models.Model):
    main_receive = models.ForeignKey(
        MainStoreToSupplierReceive,
        related_name='items',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        ItemMaster,
        on_delete=models.CASCADE,
        related_name='supplier_returns'
    )
    unit_price = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        related_name='supplier_returns'
    )
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.item} for Return ID {self.main_receive.id}"
    
class StoreToStoreReturn(models.Model):
    main_receive = models.ForeignKey(
        MainStoreToStoreReceive,
        related_name='items',
        on_delete=models.CASCADE
    )
    item = models.ForeignKey(
        ItemMaster,
        on_delete=models.CASCADE,
        related_name='store_returns'
    )
    unit_price = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        related_name='store_returns'
    )
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.quantity} of {self.item} for Return ID {self.main_receive.id}" 

class StoreToSupplierWPO(models.Model):
    PURCHASE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    store = models.ForeignKey(Store, related_name='purchases_without_po', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='supplies_without_po', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='store_purchases_without_po')
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=PURCHASE_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):       
        self.total_price = self.quantity * self.unit_price
        super(StoreToSupplierWPO, self).save(*args, **kwargs)
    def __str__(self):
        return f"Purchase of {self.item} by {self.store} from {self.supplier} - Status: {self.status}"


class StockAdjustmentReason(models.Model):
    REASON_CHOICES = [
        ("discrepancy", "Inventory Discrepancy"),
        ("damage", "Damaged Goods"),
        ("expiration", "Expired Goods"),
        ("theft", "Theft or Loss"),
        ("promotion", "Promotions or Samples"),
        ("returns", "Returns Adjustment"),
    ]

    reason_code = models.CharField(max_length=50, choices=REASON_CHOICES, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.get_reason_code_display()

class ManualStockAdjustment(models.Model):
    stock_item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="adjustments")
    adjusted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    adjustment_date = models.DateTimeField(auto_now_add=True)
    adjustment_reason = models.ForeignKey(StockAdjustmentReason, on_delete=models.SET_NULL, null=True, blank=True)
    quantity_adjusted = models.IntegerField()
    new_quantity = models.IntegerField()
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ["-adjustment_date"]
    def save(self, *args, **kwargs):
        if self.new_quantity is None:
            self.new_quantity = self.stock_item.current_quantity + self.quantity_adjusted
        super().save(*args, **kwargs)
        self.stock_item.current_quantity = self.new_quantity
        self.stock_item.save()
    def __str__(self):
        return f"Adjustment for {self.stock_item.name} on {self.adjustment_date}"

class ItemConsumption(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='item_consumptions')
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='consumptions')
    date = models.DateField(auto_now_add=True)
    quantity_consumed = models.PositiveIntegerField()
    class Meta:
        unique_together = ('store', 'item', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.store.name} - {self.item.name} - {self.quantity_consumed} on {self.date}"

class StockTaken(models.Model):
    STATUS_CHOICES = [
        ('StockUsage', 'Stock Usage'),
        ('StockSales', 'Stock Sales'),
        ('StockTransport', 'Stock Transport'),
        ('StockWastage', 'Stock Wastage'),
    ]    
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='stock_taken')
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='stock_taken')
    quantity = models.PositiveIntegerField(help_text="Total quantity of item recorded during stock audit")
    date_taken = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_taken_created_by')
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='stock_taken_updated_by')
    status_type = models.CharField(max_length=20, choices=STATUS_CHOICES, default='StockUsage')
    def __str__(self):
        return f"Stock taken for {self.item.name} on {self.date_taken}"        

class PointofSale(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='pos_sales')
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='pos_sales')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    unit_price = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='sub_requests')
    sale_price = models.DecimalField(max_digits=10, decimal_places=2) 
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.total_amount = self.sale_price * self.quantity
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.item.name} sold at {self.sale_price} each in {self.store.name}"
    
class ThirdPartySale(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='third_party_sales')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='sales')
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='third_party_sales')
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)  
    unit_price = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='sub_requests')
    revenue_percentage = models.DecimalField(max_digits=5, decimal_places=2, help_text="Percentage of revenue kept by store")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_payment = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount to be paid to the supplier")
    sale_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        self.total_amount = self.sale_price * self.quantity
        self.supplier_payment = self.total_amount * (1 - (self.revenue_percentage / 100))
        super().save(*args, **kwargs)
    def __str__(self):
        return f"Third-Party Sale: {self.item.name} sold at {self.sale_price} each in {self.store.name}"    
    
class WasteCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name             
    
class WasteRecord(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='waste_records')
    waste_category = models.ForeignKey('WasteCategory', on_delete=models.CASCADE, related_name='waste_records')
    quantity_wasted = models.PositiveIntegerField()
    date_recorded = models.DateTimeField(default=timezone.now)
    description = models.TextField(null=True, blank=True) 
    def __str__(self):
        return f"Waste: {self.item.name} - {self.quantity_wasted} {self.item.unit}"    
    
class Brand(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='waste_records')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name    

class Size(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='waste_records')
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name


class PlacementCategory(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='waste_records')
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.name


class PriceTier(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='waste_records')    
    name = models.CharField(max_length=255) 
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.name} - {self.min_price} to {self.max_price}"

class ItemPosition(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='vendor_mappings')
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='entries')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='waste_records')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='waste_records')
    pricetier = models.ForeignKey(PriceTier, on_delete=models.CASCADE, related_name='waste_records')
    placementcategory = models.ForeignKey(PlacementCategory, on_delete=models.CASCADE, related_name='waste_records')
    placement_location = models.CharField(max_length=255)  
    stock_quantity = models.PositiveIntegerField()  
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} - {self.store.name} ({self.placement_location})"
    
class Delivery(models.Model):
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='deliveries')
    delivery_date = models.DateField()
    delivery_status = models.CharField(max_length=100, choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Discrepancies', 'Discrepancies')])
    total_expected = models.IntegerField()  
    total_received = models.IntegerField()  

    def __str__(self):
        return f"Delivery from {self.supplier.name} on {self.delivery_date}"
    
class EntryMethod(models.Model):
    name = models.CharField(max_length=100, choices=[('Manual', 'Manual'), ('Automated', 'Automated')])
    description = models.TextField(null=True, blank=True)  
    
    def __str__(self):
        return self.name
    
class PhysicalItemEntry(models.Model):
    delivery = models.ForeignKey('Delivery', on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='entries')
    unit_price = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='sub_requests')
    quantity_expected = models.IntegerField() 
    quantity_received = models.IntegerField() 
    condition = models.CharField(max_length=100, choices=[('Good', 'Good'), ('Damaged', 'Damaged'), ('Expired', 'Expired')])
    entry_method = models.ForeignKey('EntryMethod', on_delete=models.CASCADE, related_name='entries')
    discrepancy_flagged = models.BooleanField(default=False)  
    discrepancy_notes = models.TextField(null=True, blank=True)  

    def __str__(self):
        return f"{self.item.name} - {self.quantity_received} received"
    
class Discrepancy(models.Model):
    entry = models.ForeignKey('PhysicalItemEntry', on_delete=models.CASCADE, related_name='discrepancies')
    discrepancy_type = models.CharField(max_length=100, choices=[('Missing', 'Missing'), ('Damaged', 'Damaged'), ('Incorrect', 'Incorrect')])
    quantity_discrepancy = models.IntegerField() 
    resolution_status = models.CharField(max_length=100, choices=[('Unresolved', 'Unresolved'), ('Resolved', 'Resolved')])
    notes = models.TextField(null=True, blank=True) 
    def __str__(self):
        return f"Discrepancy for({self.discrepancy_type})"   
    
class NewProduct(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class ProductionConversion(models.Model):
    product = models.ForeignKey(NewProduct, on_delete=models.CASCADE, related_name="production_conversions")
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="production_items")
    unit_price = models.ForeignKey(Pack, on_delete=models.CASCADE, related_name='sub_requests')
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2) 
    produced_quantity = models.DecimalField(max_digits=10, decimal_places=2) 
    production_date = models.DateField()
    total_cost = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def calculate_cost(self):
        """Calculate cost of production for the given quantity."""
        self.total_cost = self.quantity_required * self.item.cost_per_unit * self.produced_quantity
        self.save()
        return self.total_cost
    def __str__(self):
        return f"{self.produced_quantity} {self.product.name} produced on {self.production_date}"
    
    
class BillOfMaterials(models.Model):
    product = models.ForeignKey(NewProduct, on_delete=models.CASCADE, related_name="bom_entries")
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="used_in_products")
    quantity_required = models.DecimalField(max_digits=10, decimal_places=2)  
    unit = models.CharField(max_length=20, default="units")  
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def calculate_item_cost(self):
        """Calculate the cost of this item based on the quantity required."""
        return self.quantity_required * self.item.cost_per_unit

    def __str__(self):
        return f"{self.quantity_required} {self.unit} of {self.item.name} for {self.product.name}"
                                                               
# ================================end Alimni==========================================    

unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests')
unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests')
    
unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    

        