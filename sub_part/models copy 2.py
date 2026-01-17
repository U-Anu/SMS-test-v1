

class Company(models.Model):
    name = models.CharField(max_length=255, unique=True)
    registration_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

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

    def __str__(self):
        return f"{self.name} - {self.company.name}"


class ItemCategory(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='categories') 
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

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

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class ItemMaster(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='items') 
    item_code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ItemSubCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='items') 
    supplier = models.ForeignKey('Supplier', on_delete=models.SET_NULL, null=True, blank=True, related_name='items')

    def __str__(self):
        return f"{self.name} ({self.item_code})"

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True) 
    abbreviation = models.CharField(max_length=10, unique=True) 
 
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"

class ItemUnit(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="units")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT)  
    conversion_factor_to_base = models.DecimalField(max_digits=10, decimal_places=4) 

    class Meta:
        unique_together = ("item", "unit")  

    def __str__(self):
        return f"{self.item.name} - {self.unit.name}"
    
class PriceStructure(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="price_structures")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT) 
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)  

    class Meta:
        unique_together = ("item", "unit", "effective_date")

    def __str__(self):
        return f"{self.item.name} - {self.unit.name}: {self.price_per_unit}"

class Pack(models.Model):
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name="packs")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT) 
    quantity = models.PositiveIntegerField()
    pack_price = models.DecimalField(max_digits=10, decimal_places=2)  
  
    class Meta:
        unique_together = ("item", "unit", "quantity", "effective_date") 

    def __str__(self):
        return f"{self.item.name} - {self.quantity} {self.unit.name} pack: {self.pack_price}"
 


class Supplier(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='Supplier_branch')  
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    services_or_products = models.TextField(null=True, blank=True)
    contract_start_date = models.DateField(null=True, blank=True)
    contract_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=[('active', 'Active'),('inactive', 'Inactive'),],default='active',)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


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


    def __str__(self):
        return self.name


class SupplierStoreMapping(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE, related_name='SupplierStoreMapping_mappings') 
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='store_mappings') 
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_mappings') 
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('Supplier', 'store')

    def __str__(self):
        return f"{self.supplier.name} - {self.store.name}"

class PackNameMaster(models.Model):
    pack_name = models.CharField(max_length=100, unique=True, help_text="Name of the pack (e.g., Box, Bundle)")
    pack_size = models.PositiveIntegerField(help_text="Number of pieces in the pack")
    description = models.TextField(null=True, blank=True, help_text="Additional details about the pack")
  

    def __str__(self):
        return f"{self.pack_name} ({self.pack_size} pieces)"

class ItemPackSize(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='pack_sizes')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='item_pack_sizes')
    pack_name = models.ForeignKey('PackNameMaster', on_delete=models.CASCADE, related_name='item_pack_sizes', help_text="Reference to the Pack Name Master")
    quantity_per_pack = models.PositiveIntegerField(help_text="Number of pieces per pack")
    price_per_pack = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for the entire pack")
    price_per_piece = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Optional price for a single piece")

    def __str__(self):
        return f"{self.item.name} - {self.pack_name.pack_name} ({self.quantity_per_pack} pcs)"
    class Meta:
        unique_together = ('item', 'supplier', 'pack_name')

class MainStoreToSupplierRequest(models.Model):
    store = models.ForeignKey(Store, related_name='supplier_returns', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='returns', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'),('Approved', 'Approved'),('Rejected', 'Rejected'),('Completed', 'Completed'),], default='Pending')


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
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)


    def __str__(self):
        return f"{self.quantity} of {self.item} for Request ID {self.main_request.id}"    

class MainStoreToSupplierReceive(models.Model):
    store = models.ForeignKey(Store,related_name='supplier_returns_received',on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Rejected', 'Rejected'), ('Completed', 'Completed')], default='Pending')


    def __str__(self):
        return f"Return Received by {self.store}"
    
class SubStoreToSupplierReceive(models.Model):
    main_receive = models.ForeignKey(MainStoreToSupplierReceive, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='received_items') 
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack") 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.item} for Receive ID {self.main_receive.id}"    

class MainStoreToStoreRequest(models.Model):
    sending_store = models.ForeignKey(Store, related_name='store_requests_sent', on_delete=models.CASCADE) 
    receiving_store = models.ForeignKey(Store, related_name='store_requests_received', on_delete=models.CASCADE) 
    status = models.CharField(max_length=50,choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Completed', 'Completed')],default='Pending')

    def __str__(self):
        return f"Request from {self.sending_store} to {self.receiving_store}"
    
class SubStoreToStoreRequest(models.Model):
    main_request = models.ForeignKey(MainStoreToStoreRequest, related_name='items', on_delete=models.CASCADE) 
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='store_to_store_items') 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)

    def __str__(self):
        return f"{self.item} for Request ID {self.main_request.id}"    

class MainStoreToStoreReceive(models.Model):
    receiving_store = models.ForeignKey(Store, related_name='receives_initiated', on_delete=models.CASCADE) 
    sending_store = models.ForeignKey(Store, related_name='receives_sent', on_delete=models.CASCADE) 
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Received', 'Received'), ('Rejected', 'Rejected'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"Receive Record: {self.receiving_store} from {self.sending_store}"
    
class SubStoreToStoreReceive(models.Model):
    main_receive = models.ForeignKey(MainStoreToStoreReceive, related_name='items', on_delete=models.CASCADE) 
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='store_to_store_received_items') 
    quantity = models.PositiveIntegerField(help_text="Quantity received") 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} of {self.item} for Receive ID {self.main_receive.id}"     


class StoreToSupplierReturn(models.Model):
    main_receive = models.ForeignKey(MainStoreToSupplierReceive, related_name='items', on_delete=models.CASCADE) 
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='supplier_returns') 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")

    def __str__(self):
        return f"{self.quantity} of {self.item} for Return ID {self.main_receive.id}"
    
class StoreToStoreReturn(models.Model):
    main_receive = models.ForeignKey(MainStoreToStoreReceive, related_name='items', on_delete=models.CASCADE) 
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='store_returns') 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    quantity = models.PositiveIntegerField(help_text="Number of pieces per pack")

    def __str__(self):
        return f"{self.quantity} of {self.item} for Return ID {self.main_receive.id}" 

class StoreToSupplierWPO(models.Model):
    PURCHASE_STATUS_CHOICES = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    store = models.ForeignKey(Store, related_name='purchases_without_po', on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, related_name='supplies_without_po', on_delete=models.CASCADE)
    item = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='store_purchases_without_po')
    quantity = models.PositiveIntegerField()
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    purchase_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=PURCHASE_STATUS_CHOICES, default='Pending')
 
    def save(self, *args, **kwargs):       
        self.total_price = self.quantity * self.unit_price
        super(StoreToSupplierWPO, self).save(*args, **kwargs)
    def __str__(self):
        return f"Purchase of {self.item} by {self.store} from {self.supplier} - Status: {self.status}"

class StoreSellingPrice(models.Model):
    item = models.ForeignKey('ItemMaster', on_delete=models.CASCADE, related_name='pack_sizes')
    store = models.ForeignKey('Store', related_name='supplier_returns_received', on_delete=models.CASCADE)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    unit_price = models.ForeignKey('Pack', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    unit_pack = models.ForeignKey('PriceStructure', on_delete=models.CASCADE, related_name='sub_requests', null=True, blank=True)
    def __str__(self):
        return f"{self.item} - {self.store} ({self.unit_price} unit(s)) - Price: {self.selling_price}"

class StockAdjustmentReason(models.Model):
    REASON_CHOICES = [("discrepancy", "Inventory Discrepancy"), ("damage", "Damaged Goods"), ("expiration", "Expired Goods"), ("theft", "Theft or Loss"), ("promotion", "Promotions or Samples"), ("returns", "Returns Adjustment")]
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

