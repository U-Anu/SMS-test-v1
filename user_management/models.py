# from django.db import models
# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
# from django.utils import timezone

# # Create your models here.
# # ------------------------- CRM Start---------------------------------------

# class LeadSource(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.name
# class Lead(models.Model):
#     name = models.CharField(max_length=255)
#     company = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     project_description = models.TextField()
#     source = models.ForeignKey(LeadSource, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=50, choices=[('new', 'New'), ('qualified', 'Qualified'), ('disqualified', 'Disqualified')])
#     budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     urgency = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
#     decision_maker = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     assigned_to = models.ForeignKey('SalesRepresentative', on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return self.name
# class SalesRepresentative(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=20)

#     def __str__(self):
#         return self.name
# class ClientInteractionType(models.Model):
#     type_name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.type_name
# class ClientInteraction(models.Model):
#     lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
#     interaction_type = models.ForeignKey(ClientInteractionType, on_delete=models.SET_NULL, null=True)
#     description = models.TextField()
#     date = models.DateTimeField(auto_now_add=True)
#     follow_up_date = models.DateTimeField(null=True, blank=True)
#     engagement_metrics = models.JSONField(null=True, blank=True)  # To store open rates, response time, etc.

#     def __str__(self):
#         return f"{self.interaction_type} with {self.lead.name}"
# class SalesStage(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name
# class Opportunity(models.Model):
#     lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
#     stage = models.ForeignKey(SalesStage, on_delete=models.SET_NULL, null=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     probability = models.IntegerField()  # Probability to close the deal (0 to 100%)
#     expected_close_date = models.DateField()
#     assigned_to = models.ForeignKey(SalesRepresentative, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return f"Opportunity with {self.lead.name} - {self.stage.name}"
# class Proposal(models.Model):
#     opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
#     created_date = models.DateTimeField(auto_now_add=True)
#     proposal_file = models.FileField(upload_to='proposals/')  # Uploaded file
#     status = models.CharField(max_length=50, choices=[('sent', 'Sent'), ('viewed', 'Viewed'), ('negotiation', 'In Negotiation'), ('approved', 'Approved')])
#     negotiation_notes = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Proposal for {self.opportunity.lead.name}"
# class Contract(models.Model):
#     opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
#     contract_file = models.FileField(upload_to='contracts/')
#     signed = models.BooleanField(default=False)
#     signed_date = models.DateField(null=True, blank=True)
#     renewal_date = models.DateField(null=True, blank=True)  # For ongoing services
#     obligations = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Contract for {self.opportunity.lead.name}"
# class Project(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     project_name = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     progress = models.IntegerField(choices=[(0, 'Not Started'), (1, 'In Progress'), (2, 'Completed')], default=0)
#     milestone_tracking = models.JSONField(null=True, blank=True)  # Track project milestones in a JSON format
#     manager = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='managed_projects')
    
#     def __str__(self):
#         return self.project_name
    
# class ProjectCommunication(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     communication_date = models.DateTimeField(auto_now_add=True)
#     message = models.TextField()
#     file_attachment = models.FileField(upload_to='communications/', null=True, blank=True)  # Optional file upload

#     def __str__(self):
#         return f"Communication for {self.project.project_name}"
# class ClientFollowUp(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     follow_up_date = models.DateField()
#     message = models.TextField()
#     action_taken = models.CharField(max_length=255, choices=[('email_sent', 'Email Sent'), ('called', 'Called')])

#     def __str__(self):
#         return f"Follow-up for {self.project.project_name} on {self.follow_up_date}"
# class ClientSatisfactionSurvey(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     sent_date = models.DateField(auto_now_add=True)
#     client_feedback = models.TextField()
#     score = models.IntegerField(choices=[(1, 'Very Dissatisfied'), (2, 'Dissatisfied'), (3, 'Neutral'), (4, 'Satisfied'), (5, 'Very Satisfied')])

#     def __str__(self):
#         return f"Survey for {self.project.project_name}"



# # ------------------------- CRM End---------------------------------------

# #--------------------------- Subcontractor Management Start-----------------------
# class Subcontractor(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     address = models.TextField()
#     qualification_documents = models.FileField(upload_to='qualifications/', blank=True, null=True)
#     certification = models.CharField(max_length=255)
#     experience_years = models.IntegerField()
#     financial_stability_rating = models.IntegerField()  # Rating scale of 1-10
#     references = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=100, choices=(('Prequalified', 'Prequalified'), ('Pending', 'Pending'), ('Rejected', 'Rejected')))
#     date_prequalified = models.DateField(blank=True, null=True)
    
#     def __str__(self):
#         return self.name
    
# class Expertise(models.Model):
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     area_of_expertise = models.CharField(max_length=255)  # e.g., Electrical, Plumbing, Roofing
#     certifications = models.CharField(max_length=255, blank=True, null=True)
#     performance_rating = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)  # A rating out of 5 for performance reviews
    
#     def __str__(self):
#         return f"{self.subcontractor.name} - {self.area_of_expertise}"


# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField(blank=True, null=True)
#     budget = models.DecimalField(max_digits=12, decimal_places=2)
#     location = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.name
    
# class Bid(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     bid_amount = models.DecimalField(max_digits=12, decimal_places=2)
#     bid_submission_date = models.DateField()
#     status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')))
#     notes = models.TextField(blank=True, null=True)
    
#     def __str__(self):
#         return f"Bid by {self.subcontractor.name} for {self.project.name}"
    
# class SubcontractorContract(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     contract_file = models.FileField(upload_to='contracts/')
#     signed_date = models.DateField()
#     payment_terms = models.TextField()  # Payment schedule and conditions
#     insurance_requirements = models.TextField(blank=True, null=True)
#     change_order_provision = models.TextField(blank=True, null=True)
#     termination_conditions = models.TextField(blank=True, null=True)
    
#     def __str__(self):
#         return f"Contract for {self.subcontractor.name} in {self.project.name}"

# class Task(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     task_name = models.CharField(max_length=255)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Delayed', 'Delayed')))
    
#     def __str__(self):
#         return f"Task {self.task_name} for {self.subcontractor.name} in {self.project.name}"

# class PerformanceReport(models.Model):
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     report_date = models.DateField()
#     tasks_completed = models.IntegerField(default=0)
#     issues_encountered = models.TextField(blank=True, null=True)
#     safety_compliance = models.BooleanField(default=True)
#     site_photos = models.ImageField(upload_to='site_photos/', blank=True, null=True)
    
#     def __str__(self):
#         return f"Performance Report for {self.subcontractor.name} on {self.report_date}"

# class Payment(models.Model):
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     milestone = models.CharField(max_length=255)
#     payment_due = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_date = models.DateField(blank=True, null=True)
#     status = models.CharField(max_length=100, choices=(('Pending', 'Pending'), ('Paid', 'Paid'), ('Delayed', 'Delayed')))
    
#     def __str__(self):
#         return f"Payment for {self.subcontractor.name} in {self.project.name}"

# class ChangeOrder(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     change_description = models.TextField()
#     additional_cost = models.DecimalField(max_digits=12, decimal_places=2)
#     new_completion_date = models.DateField(blank=True, null=True)
#     status = models.CharField(max_length=100, choices=(('Requested', 'Requested'), ('Approved', 'Approved'), ('Rejected', 'Rejected')))
    
#     def __str__(self):
#         return f"Change Order for {self.subcontractor.name} in {self.project.name}"


# class ProjectCloseout(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     subcontractor = models.ForeignKey(Subcontractor, on_delete=models.CASCADE)
#     final_inspection_date = models.DateField()
#     punch_list_items = models.TextField(blank=True, null=True)
#     punch_list_completed = models.BooleanField(default=False)
#     final_payment = models.DecimalField(max_digits=12, decimal_places=2)
#     closeout_documents = models.FileField(upload_to='closeout_documents/', blank=True, null=True)
    
#     def __str__(self):
#         return f"Closeout for {self.subcontractor.name} in {self.project.name}"

# #--------------------------- Subcontractor Management END-----------------------

# #--------------------------- Field Management System Start-----------------------
# class Role(models.Model):
#     name = models.CharField(max_length=50)

#     def __str__(self):
#         return self.name
    
# class CustomUser(AbstractUser):
#     role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
#     mobile_device_id = models.CharField(max_length=100, blank=True, null=True)  # For tracking mobile device usage

#     def __str__(self):
#         return self.username

# class Project(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField()
#     project_manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='managed_projects')
#     documents = models.FileField(upload_to='project_documents/', blank=True, null=True)  # Project Blueprints, Safety Protocols

#     def __str__(self):
#         return self.name

# class TeamMember(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     role = models.CharField(max_length=50, choices=[('Manager', 'Manager'), ('Worker', 'Worker'), ('Subcontractor', 'Subcontractor')])
#     permissions = models.TextField()  # Detailed permissions for each user within the project

#     def __str__(self):
#         return f"{self.user.username} - {self.role} ({self.project.name})"
    
# class Task(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     assigned_to = models.ManyToManyField(TeamMember)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     completion_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

#     def __str__(self):
#         return f"{self.name} - {self.project.name}"

# class DailyProgressReport(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     report_date = models.DateField(auto_now_add=True)
#     description = models.TextField()  # Task details e.g., "Pouring foundation 80% complete"
#     worker_count = models.IntegerField()
#     machinery_in_use = models.CharField(max_length=255)
#     materials_used = models.TextField()  # Can be linked with material management later
#     completion_percentage = models.DecimalField(max_digits=5, decimal_places=2)

#     def __str__(self):
#         return f"Report for {self.task.name} - {self.report_date}"
# class PhotoDocumentation(models.Model):
#     task = models.ForeignKey(Task, on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='task_photos/')
#     description = models.TextField(blank=True, null=True)
#     geo_tag = models.CharField(max_length=255, blank=True, null=True)  # Geo-tag information
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Photo for {self.task.name} - {self.timestamp}"
# class Issue(models.Model):
#     ISSUE_TYPES = [
#         ('Safety', 'Safety'),
#         ('Quality', 'Quality'),
#         ('Equipment', 'Equipment'),
#         ('Other', 'Other'),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     issue_type = models.CharField(max_length=50, choices=ISSUE_TYPES)
#     description = models.TextField()
#     photo = models.ImageField(upload_to='issue_photos/', blank=True, null=True)
#     status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('In Progress', 'In Progress'), ('Resolved', 'Resolved')], default='Open')
#     assigned_to = models.ForeignKey(TeamMember, on_delete=models.SET_NULL, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.issue_type} - {self.project.name}"
# class Message(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     recipients = models.ManyToManyField(CustomUser, related_name='messages_received')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Message from {self.sender.username} in {self.project.name}"

# class Notification(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     message = models.CharField(max_length=255)
#     is_read = models.BooleanField(default=False)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notification for {self.user.username} - {self.message}"
# class Milestone(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateField()
#     is_completed = models.BooleanField(default=False)
#     approved_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

#     def __str__(self):
#         return f"{self.name} - {self.project.name}"
# class Material(models.Model):
#     name = models.CharField(max_length=255)
#     unit = models.CharField(max_length=50)
#     quantity = models.DecimalField(max_digits=10, decimal_places=2)

#     def __str__(self):
#         return self.name

# class StockAdjustment(models.Model):
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     adjusted_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     quantity_adjusted = models.DecimalField(max_digits=10, decimal_places=2)
#     reason = models.CharField(max_length=255)
#     adjustment_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Stock Adjustment for {self.material.name}"

# class StockReplenishmentRequest(models.Model):
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     requested_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     quantity_requested = models.DecimalField(max_digits=10, decimal_places=2)
#     request_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return f"Replenishment Request for {self.material.name} - {self.project.name}"


# #--------------------------- Field Management System END-----------------------

# # -------------------------  Inventory Management Models Start---------------------------------------

# # Master Models
# class Supplier(models.Model):
#     name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField()
#     address = models.TextField()
    
#     def __str__(self):
#         return self.name

# class Warehouse(models.Model):
#     location = models.CharField(max_length=255)
#     capacity = models.IntegerField()  # Total storage capacity
    
#     def __str__(self):
#         return self.location

# class ItemCategory(models.Model):
#     name = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.name

# # Inventory Item Model
# class Item(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
#     supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
#     stock_quantity = models.IntegerField(default=0)
#     reorder_point = models.IntegerField(default=10)
#     safety_stock = models.IntegerField(default=5)
#     price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
#     warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     barcode = models.CharField(max_length=255, unique=True)
    
#     def __str__(self):
#         return self.name

# # Stock Movement Model
# class StockEntry(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     movement_type = models.CharField(max_length=10, choices=[('IN', 'Stock In'), ('OUT', 'Stock Out')])
#     date = models.DateTimeField(default=timezone.now)
    
#     def __str__(self):
#         return f"{self.item.name} - {self.movement_type} - {self.quantity}"

# # Requisition Model
# class Requisition(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     requested_by = models.CharField(max_length=255)
#     date_requested = models.DateTimeField(default=timezone.now)
#     date_fulfilled = models.DateTimeField(null=True, blank=True)
    
#     def __str__(self):
#         return f"Requisition for {self.item.name}"

# # Inventory Audit Model
# class InventoryAudit(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.CASCADE)
#     audit_date = models.DateTimeField(default=timezone.now)
#     physical_count = models.IntegerField()
#     system_count = models.IntegerField()
#     discrepancy = models.IntegerField()
#     comments = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Audit for {self.item.name} on {self.audit_date}"
    
#     # Master Models for Equipment
# class EquipmentCategory(models.Model):
#     name = models.CharField(max_length=255)
    
#     def __str__(self):
#         return self.name

# class Equipment(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(EquipmentCategory, on_delete=models.CASCADE)
#     serial_number = models.CharField(max_length=255, unique=True)
#     purchase_date = models.DateField()
#     condition = models.CharField(max_length=255, choices=[('New', 'New'), ('Used', 'Used')])
#     location = models.ForeignKey(Warehouse, on_delete=models.CASCADE)  # Storage location
#     status = models.CharField(max_length=255, choices=[('Available', 'Available'), ('In Use', 'In Use'), ('Under Maintenance', 'Under Maintenance')])

#     def __str__(self):
#         return self.name

# # Equipment Assignment
# class EquipmentAssignment(models.Model):
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
#     assigned_to = models.CharField(max_length=255)
#     assigned_date = models.DateTimeField(default=timezone.now)
#     return_date = models.DateTimeField(null=True, blank=True)
    
#     def __str__(self):
#         return f"{self.equipment.name} assigned to {self.assigned_to}"

# # Equipment Maintenance
# class EquipmentMaintenance(models.Model):
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
#     maintenance_date = models.DateTimeField(default=timezone.now)
#     maintenance_type = models.CharField(max_length=255, choices=[('Preventive', 'Preventive'), ('Corrective', 'Corrective')])
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     notes = models.TextField()

#     def __str__(self):
#         return f"Maintenance for {self.equipment.name} on {self.maintenance_date}"

# # Equipment Audit
# class EquipmentAudit(models.Model):
#     equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
#     audit_date = models.DateTimeField(default=timezone.now)
#     condition = models.CharField(max_length=255)
#     comments = models.TextField(null=True, blank=True)
    
#     def __str__(self):
#         return f"Audit for {self.equipment.name} on {self.audit_date}"


# # Asset Category Model
# class AssetCategory(models.Model):
#     name = models.CharField(max_length=255)

#     def __str__(self):
#         return self.name

# # Asset Model
# class Asset(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(AssetCategory, on_delete=models.CASCADE)
#     purchase_date = models.DateField()
#     purchase_cost = models.DecimalField(max_digits=12, decimal_places=2)
#     depreciation_rate = models.DecimalField(max_digits=5, decimal_places=2)
#     location = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
#     assigned_to = models.CharField(max_length=255, null=True, blank=True)
#     status = models.CharField(max_length=255, choices=[('Active', 'Active'), ('Retired', 'Retired')])

#     def __str__(self):
#         return self.name

# # Asset Maintenance Model
# class AssetMaintenance(models.Model):
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
#     maintenance_date = models.DateTimeField(default=timezone.now)
#     maintenance_type = models.CharField(max_length=255)
#     cost = models.DecimalField(max_digits=10, decimal_places=2)
#     notes = models.TextField()

#     def __str__(self):
#         return f"Maintenance for {self.asset.name}"

# # Asset Depreciation Model
# class Depreciation(models.Model):
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
#     depreciation_date = models.DateTimeField(default=timezone.now)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
    
#     def __str__(self):
#         return f"Depreciation for {self.asset.name}"

# # Asset Audit Model
# class AssetAudit(models.Model):
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
#     audit_date = models.DateTimeField(default=timezone.now )
#     condition = models.CharField(max_length=255)
#     comments = models.TextField()

#     def __str__(self):
#         return f"Audit for {self.asset.name}"


# # -------------------------  Inventory Management Models END---------------------------------------


# # ----------------------------- Budget & Financial Management Start------------------- 

# class Vendor(models.Model):
#     name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField()
#     address = models.TextField()

#     def __str__(self):
#         return self.name

# class Customer(models.Model):
#     name = models.CharField(max_length=255)
#     contact_person = models.CharField(max_length=255)
#     phone = models.CharField(max_length=15)
#     email = models.EmailField()
#     address = models.TextField()

#     def __str__(self):
#         return self.name

# class Account(models.Model):
#     ACCOUNT_TYPE_CHOICES = (
#         ('asset', 'Asset'),
#         ('liability', 'Liability'),
#         ('equity', 'Equity'),
#         ('revenue', 'Revenue'),
#         ('expense', 'Expense'),
#     )

#     name = models.CharField(max_length=255)
#     account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES)
#     balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"{self.name} ({self.account_type})"

# class Currency(models.Model):
#     name = models.CharField(max_length=255)
#     symbol = models.CharField(max_length=5)
#     exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, help_text="Exchange rate to the base currency")

#     def __str__(self):
#         return self.name
    

# #Cost Estimation & Budgeting
# class Budget(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     total_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     allocated_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     remaining_budget = models.DecimalField(max_digits=15, decimal_places=2)
#     currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)

#     def __str__(self):
#         return f"Budget for {self.project.name}"

# class CostCategory(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()

#     def __str__(self):
#         return self.name

# class CostEstimation(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     category = models.ForeignKey(CostCategory, on_delete=models.SET_NULL, null=True)
#     estimated_cost = models.DecimalField(max_digits=15, decimal_places=2)
#     actual_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
#     forecast_cost = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.category.name} for {self.project.name}"

# #Financial Management 
# class FinancialTransaction(models.Model):
#     TRANSACTION_TYPE_CHOICES = (
#         ('debit', 'Debit'),
#         ('credit', 'Credit'),
#     )
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE)
#     transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     description = models.TextField(null=True, blank=True)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.transaction_type} of {self.amount} in {self.project.name} to {self.account.name}"

# class Expense(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="expenses")
#     vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
#     description = models.TextField()
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     date = models.DateField()
#     approved_by = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Expense of {self.amount} for {self.project.name}"

# class Revenue(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     description = models.TextField()
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     date = models.DateField()
#     received_by = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Revenue of {self.amount} for {self.project.name}"

# # Billing & Invoicing
# class Invoice(models.Model):
#     INVOICE_STATUS_CHOICES = (
#         ('draft', 'Draft'),
#         ('sent', 'Sent'),
#         ('paid', 'Paid'),
#         ('overdue', 'Overdue'),
#     )

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
#     invoice_number = models.CharField(max_length=50, unique=True)
#     issue_date = models.DateField()
#     due_date = models.DateField()
#     status = models.CharField(max_length=10, choices=INVOICE_STATUS_CHOICES, default='draft')
#     total_amount = models.DecimalField(max_digits=15, decimal_places=2)
#     paid_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f"Invoice {self.invoice_number} for {self.project.name}"

# class Payment(models.Model):
#     invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     payment_date = models.DateField()
#     payment_method = models.CharField(max_length=255)
#     reference_number = models.CharField(max_length=255, null=True, blank=True)

#     def __str__(self):
#         return f"Payment of {self.amount} for invoice {self.invoice.invoice_number}"

# class MilestoneBilling(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     milestone_name = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)
#     due_date = models.DateField()
#     amount = models.DecimalField(max_digits=15, decimal_places=2)
#     invoiced = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Milestone Billing for {self.project.name}: {self.milestone_name}"

# # ----------------------------- Budget & Financial Management End------------------- 

# # ----------------------------- Risk Management Start------------------- 

# class RiskCategory(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return self.name

# class RiskOwner(models.Model):
#     name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name
    
# #risk management
# class Risk(models.Model):
#     RISK_TYPE_CHOICES = (
#         ('financial', 'Financial'),
#         ('operational', 'Operational'),
#         ('compliance', 'Compliance'),
#         ('strategic', 'Strategic'),
#         ('safety', 'Safety'),
#     )

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     risk_category = models.ForeignKey(RiskCategory, on_delete=models.SET_NULL, null=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     risk_type = models.CharField(max_length=50, choices=RISK_TYPE_CHOICES)
#     date_identified = models.DateField(auto_now_add=True)
#     owner = models.ForeignKey(RiskOwner, on_delete=models.SET_NULL, null=True)
#     status = models.CharField(max_length=50, default='Open')

#     def __str__(self):
#         return f"{self.name} ({self.project.name})"

# class RiskAssessment(models.Model):
#     RISK_PROBABILITY_CHOICES = (
#         (1, 'Very Low'),
#         (2, 'Low'),
#         (3, 'Medium'),
#         (4, 'High'),
#         (5, 'Very High'),
#     )

#     RISK_IMPACT_CHOICES = (
#         (1, 'Very Low'),
#         (2, 'Low'),
#         (3, 'Medium'),
#         (4, 'High'),
#         (5, 'Very High'),
#     )

#     risk = models.OneToOneField(Risk, on_delete=models.CASCADE)
#     probability = models.IntegerField(choices=RISK_PROBABILITY_CHOICES)
#     impact = models.IntegerField(choices=RISK_IMPACT_CHOICES)
#     overall_risk_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

#     def calculate_risk_score(self):
#         # Overall risk score is calculated as probability * impact
#         self.overall_risk_score = self.probability * self.impact
#         self.save()

#     def __str__(self):
#         return f"Assessment for {self.risk.name}"

#     def save(self, *args, **kwargs):
#         self.calculate_risk_score()
#         super().save(*args, **kwargs)

# # Mitigation Strategies
# class MitigationStrategy(models.Model):
#     risk = models.ForeignKey(Risk, on_delete=models.CASCADE)
#     strategy = models.TextField()
#     mitigation_owner = models.ForeignKey(RiskOwner, on_delete=models.SET_NULL, null=True, related_name="mitigation_owner")
#     start_date = models.DateField()
#     end_date = models.DateField()
#     status = models.CharField(max_length=50, default='Pending')

#     def __str__(self):
#         return f"Mitigation for {self.risk.name}"

# class MitigationAction(models.Model):
#     mitigation_strategy = models.ForeignKey(MitigationStrategy, on_delete=models.CASCADE)
#     action_name = models.CharField(max_length=255)
#     action_description = models.TextField()
#     due_date = models.DateField()
#     completed = models.BooleanField(default=False)
#     completed_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"Action {self.action_name} for {self.mitigation_strategy.risk.name}"

# #Risk Tracking & Monitoring
# class RiskReview(models.Model):
#     risk = models.ForeignKey(Risk, on_delete=models.CASCADE)
#     review_date = models.DateField(auto_now_add=True)
#     status = models.CharField(max_length=50, choices=[('Open', 'Open'), ('Mitigated', 'Mitigated'), ('Closed', 'Closed')])
#     comments = models.TextField(null=True, blank=True)
#     reviewed_by = models.ForeignKey(RiskOwner, on_delete=models.SET_NULL, null=True, related_name="reviewed_by")

#     def __str__(self):
#         return f"Review of {self.risk.name} on {self.review_date}"


# # ----------------------------- Risk Management End------------------- 


# # ----------------------------- Quality & Safety Management End------------------- 

# class SafetyOfficer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     designation = models.CharField(max_length=255)

#     def __str__(self):
#         return f'{self.user.get_full_name()} - {self.project.name}'

# class QualityInspector(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     designation = models.CharField(max_length=255)

#     def __str__(self):
#         return f'{self.user.get_full_name()} - {self.project.name}'

# # Planning Stage Models
# class SafetyPlan(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     content = models.TextField()  # Detailed safety plan content
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Safety Plan for {self.project.name}"

# class QualityControlPlan(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     content = models.TextField()  # Quality control plan content
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Quality Plan for {self.project.name}"

# class LegalRequirement(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     description = models.TextField()
#     requirement_type = models.CharField(max_length=255)  # e.g., OSHA, Building Code, Environmental Standards

#     def __str__(self):
#         return f"Legal Requirement for {self.project.name}: {self.requirement_type}"

# class RiskAssessment(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     description = models.TextField()
#     mitigation_plan = models.TextField()
#     risk_level = models.CharField(max_length=50, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])

#     def __str__(self):
#         return f"Risk Assessment for {self.project.name}"

# # Implementation Stage Models
# class Inspection(models.Model):
#     INSPECTION_TYPE_CHOICES = [
#         ('Safety', 'Safety'),
#         ('Quality', 'Quality'),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     inspector = models.ForeignKey(User, on_delete=models.CASCADE)  # Safety Officer or Quality Inspector
#     inspection_type = models.CharField(max_length=50, choices=INSPECTION_TYPE_CHOICES)
#     date = models.DateField()
#     checklist = models.TextField()  # List of items inspected
#     findings = models.TextField()  # Any issues or observations

#     def __str__(self):
#         return f"{self.inspection_type} Inspection for {self.project.name} on {self.date}"

# class ComplianceMonitor(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     compliance_type = models.CharField(max_length=50)  # Safety or Quality compliance
#     description = models.TextField()
#     status = models.CharField(max_length=50, choices=[('Compliant', 'Compliant'), ('Non-compliant', 'Non-compliant')])
#     date = models.DateField()

#     def __str__(self):
#         return f"{self.compliance_type} Compliance for {self.project.name} on {self.date}"

# # Incident Reporting and Response Models
# class IncidentReport(models.Model):
#     INCIDENT_TYPE_CHOICES = [
#         ('Safety', 'Safety'),
#         ('Quality', 'Quality'),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     incident_type = models.CharField(max_length=50, choices=INCIDENT_TYPE_CHOICES)
#     description = models.TextField()
#     date_reported = models.DateTimeField(auto_now_add=True)
#     immediate_action = models.TextField(null=True, blank=True)  # Actions taken immediately on-site

#     def __str__(self):
#         return f"Incident ({self.incident_type}) for {self.project.name} by {self.reported_by.get_full_name()}"

# class Investigation(models.Model):
#     incident = models.OneToOneField(IncidentReport, on_delete=models.CASCADE)
#     investigator = models.ForeignKey(User, on_delete=models.CASCADE)
#     findings = models.TextField()
#     root_cause = models.TextField()
#     investigation_date = models.DateField()

#     def __str__(self):
#         return f"Investigation for Incident {self.incident.id} by {self.investigator.get_full_name()}"

# class CorrectiveAction(models.Model):
#     incident = models.ForeignKey(IncidentReport, on_delete=models.CASCADE)
#     description = models.TextField()
#     action_taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     date_taken = models.DateField()
#     status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

#     def __str__(self):
#         return f"Corrective Action for Incident {self.incident.id}"

# # Monitoring and Audits Models
# class Audit(models.Model):
#     AUDIT_TYPE_CHOICES = [
#         ('Safety', 'Safety'),
#         ('Quality', 'Quality'),
#     ]

#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     audit_type = models.CharField(max_length=50, choices=AUDIT_TYPE_CHOICES)
#     conducted_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()
#     findings = models.TextField()

#     def __str__(self):
#         return f"{self.audit_type} Audit for {self.project.name}"

# class CorrectivePreventiveAction(models.Model):
#     audit = models.ForeignKey(Audit, on_delete=models.CASCADE)
#     description = models.TextField()
#     date_taken = models.DateField()
#     status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

#     def __str__(self):
#         return f"CAPA for Audit {self.audit.id}"

# # Continuous Improvement and Project Closeout Models
# class FinalReview(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     review_type = models.CharField(max_length=50, choices=[('Safety', 'Safety'), ('Quality', 'Quality')])
#     review_details = models.TextField()
#     conducted_by = models.ForeignKey(User, on_delete=models.CASCADE)
#     date = models.DateField()

#     def __str__(self):
#         return f"Final {self.review_type} Review for {self.project.name}"

# class CloseoutDocument(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     document_type = models.CharField(max_length=255)  # e.g., Inspection reports, safety records, certificates
#     file = models.FileField(upload_to='closeout_documents/')
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Closeout Document for {self.project.name} - {self.document_type}"

# # ----------------------------- Quality & Safety Management End------------------- 


# # ----------------------------- Contract & Change Order Management Start------------------- 

# class Client(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.TextField()
#     contact_person = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name

# class Contractor(models.Model):
#     name = models.CharField(max_length=255)
#     address = models.TextField()
#     contact_person = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name

# class Contract(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE)
#     scope_of_work = models.TextField()
#     pricing = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_terms = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     signed_by_client = models.BooleanField(default=False)
#     signed_by_contractor = models.BooleanField(default=False)
#     approved_by = models.CharField(max_length=255, null=True, blank=True)
#     status = models.CharField(max_length=50, choices=[
#         ('draft', 'Draft'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#         ('closed', 'Closed')
#     ], default='draft')

#     def __str__(self):
#         return f"Contract for {self.project.name} with {self.contractor.name}"

# class ContractMilestone(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     due_date = models.DateField()
#     completed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Milestone: {self.name} for Contract {self.contract.id}"
# class Payment(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=12, decimal_places=2)
#     payment_date = models.DateField()
#     milestone = models.ForeignKey(ContractMilestone, null=True, blank=True, on_delete=models.SET_NULL)
#     paid_by_client = models.BooleanField(default=False)
#     payment_status = models.CharField(max_length=50, choices=[
#         ('pending', 'Pending'),
#         ('completed', 'Completed'),
#         ('overdue', 'Overdue')
#     ], default='pending')

#     def __str__(self):
#         return f"Payment for {self.contract.id} - {self.amount}"
    
# class ChangeOrder(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     requestor = models.CharField(max_length=255)  # Client or contractor
#     description = models.TextField()
#     change_reason = models.TextField()
#     impact_on_scope = models.TextField()
#     cost_impact = models.DecimalField(max_digits=12, decimal_places=2)
#     time_impact = models.IntegerField(help_text="Time impact in days")
#     status = models.CharField(max_length=50, choices=[
#         ('submitted', 'Submitted'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#         ('implemented', 'Implemented')
#     ], default='submitted')
#     submitted_date = models.DateField(auto_now_add=True)
#     approved_date = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"Change Order {self.id} for Contract {self.contract.id}"

# class ChangeOrderApproval(models.Model):
#     change_order = models.OneToOneField(ChangeOrder, on_delete=models.CASCADE)
#     approved_by = models.CharField(max_length=255)
#     approval_date = models.DateField()
#     notes = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Approval for Change Order {self.change_order.id}"

# class ChangeOrderImplementation(models.Model):
#     change_order = models.OneToOneField(ChangeOrder, on_delete=models.CASCADE)
#     implementation_details = models.TextField()
#     implementation_date = models.DateField()
#     new_deadline = models.DateField(null=True, blank=True)

#     def __str__(self):
#         return f"Implementation for Change Order {self.change_order.id}"
# class ContractCloseout(models.Model):
#     contract = models.OneToOneField(Contract, on_delete=models.CASCADE)
#     closeout_date = models.DateField()
#     final_review_notes = models.TextField()
#     completed_documents = models.FileField(upload_to='contract_closeouts/')
#     signed_off_by = models.CharField(max_length=255)

#     def __str__(self):
#         return f"Closeout for Contract {self.contract.id}"
# class Document(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     change_order = models.ForeignKey(ChangeOrder, null=True, blank=True, on_delete=models.CASCADE)
#     document_name = models.CharField(max_length=255)
#     document_file = models.FileField(upload_to='documents/')
#     upload_date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.document_name
# class AuditLog(models.Model):
#     contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
#     change_order = models.ForeignKey(ChangeOrder, null=True, blank=True, on_delete=models.CASCADE)
#     action = models.CharField(max_length=255)
#     action_by = models.CharField(max_length=255)
#     action_date = models.DateTimeField(auto_now_add=True)
#     notes = models.TextField(null=True, blank=True)

#     def __str__(self):
#         return f"Audit Log for Contract {self.contract.id} - {self.action}"


# # ----------------------------- Contract & Change Order Management End------------------- 
