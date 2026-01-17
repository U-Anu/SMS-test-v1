from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
import string
import random
from datetime import timedelta
from django.utils.timezone import now


class Currency(models.Model):
    currency_id = models.CharField(max_length=10, primary_key=True, editable=False)
    currency_code = models.CharField(max_length=10, unique=True)
    currency_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    reference_id =  models.CharField(max_length=100)
    def save(self, *args, **kwargs):
        if not self.currency_id:
            self.currency_id = self.generate_unique_currency_id()
        super().save(*args, **kwargs)
    def generate_unique_currency_id(self):
        length = 10
        chars = string.ascii_uppercase + string.digits  
        while True:
            new_id = ''.join(random.choices(chars, k=length))
            if not Currency.objects.filter(currency_id=new_id).exists():  
                return new_id
    def __str__(self):
        return self.currency_code        

class SchoolRegistration(models.Model):
    school_id = models.CharField(max_length=50, unique=True)
    school_name = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    last_name = models.CharField(max_length=30)
    phone_number = models.PositiveBigIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    incorporation_number = models.PositiveBigIntegerField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    number_of_branches = models.PositiveBigIntegerField(blank=True, null=True)
    number_of_staffs = models.PositiveBigIntegerField(blank=True, null=True)
    end_of_financial_year = models.DateField(blank=False, null=True)
    end_of_month_date = models.DateField(blank=False, null=True)
    amount_rounded_to = models.IntegerField()
    local_currency = models.ForeignKey(Currency, on_delete=models.CASCADE,)
    reference_id =  models.CharField(max_length=100,null=True, blank=True)
   
     
    def __str__(self):
        return self.school_id
    


class StudentHouse(models.Model):
    name = models.CharField(max_length=50, unique=True)
    student_house = models.CharField(max_length=100,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
     
    def __str__(self):
        return self.student_house

def default_valid_until():
    current_date = datetime.now()
    valid_until_date = current_date + timedelta(days=30)
    return current_date, valid_until_date




class Purpose(models.Model):
    purpose = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.purpose


class ComplainType(models.Model):
    complain_type = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.complain_type


class Source(models.Model):
    source = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.source


class Reference(models.Model):
    reference = models.CharField(max_length=250)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.reference


class Section(models.Model):
    section_name = models.CharField(max_length=50)


    def __str__(self):
        return self.section_name



class ClassRegister(models.Model):
    Class = models.ForeignKey("Class", on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    teacher = models.ForeignKey("AddStaff", on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey("StudentAdmission", on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):  
        return f"{self.class_info} - {self.section_info}"    
    
class GuardianMaster(models.Model):
    guardian_name = models.CharField(max_length=250)
   

 

class GradingScale(models.Model):
    min_grade = models.IntegerField()
    max_grade = models.IntegerField()
    subject_grade = models.CharField(max_length=2, choices=(("A", "A"), ("A-", "A-"), ("B+", "B+"), ("B", "B"), ("B-", "B-"), ("C+", "C+"), ("C", "C"), ("C-", "C-"), ("D+", "D+"), ("D", "D"), ("D-", "D-"), ("E", "E"), ("F", "F")))


    def __str__(self):
        return self.subject_grade


class GradingSystem(models.Model):
    name = models.CharField(max_length=100)
    Class = models.ForeignKey("Class", on_delete=models.CASCADE, null=True, blank=True)  
    scale = models.IntegerField(null=True, blank=True)
    points = models.IntegerField(null=True, blank=True)
    pass_remarks = models.CharField(max_length=200) 
    fail_remarks = models.CharField(max_length=200)  
   
    def __str__(self):
        return self.name

class Class(models.Model):
    Class = models.CharField(max_length=255, null=True, blank=True)
    grading = models.ForeignKey(GradingSystem, on_delete=models.CASCADE, null=True, blank=True)
    section = models.ManyToManyField(Section)
    def __str__(self):
        return f"{self.Class}"


class AssignSubjects(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    grading = models.ForeignKey("AddGrade", on_delete=models.CASCADE, null=True, blank=True)
    section = models.ManyToManyField(Section)

    def __str__(self):
        return f"{self.name} - {self.grade}"

 

class AssignSubject(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ManyToManyField("Subjects")

    def __str__(self):
        return f"{self.name} - {self.grade}"






    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)
    head_teacher = models.ForeignKey(
        "sub_part.SchoolHeads",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="head_teacher_department",
    )

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.name



class SchoolCompositions(models.Model):
    description = models.TextField()
    no_of_years = models.IntegerField()
    Class = models.ManyToManyField(Class)


    def __str__(self):
        return self.description


class EducationLevel(models.Model):
    level = models.CharField(max_length=255)
    description = models.TextField()
    composition = models.ManyToManyField(SchoolCompositions)


    def __str__(self):
        return self.level




class SchoolYear(models.Model):
    year = models.CharField(max_length=255)
    term = models.ManyToManyField("Term")


    def __str__(self):
        return self.year

class Term(models.Model):
    term_name = models.CharField(max_length=50, choices=[("Term 1", "Term 1"), ("Term 2", "Term 2"), ("Term 3", "Term 3")])
    start_date = models.DateField()
    end_date = models.DateField()


    def __str__(self):
        return self.term_name


class StudentCategory(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category


class DisableReason(models.Model):
    name = models.CharField(max_length=50)
    

    def __str__(self):
        return self.name


class Route(models.Model):
    route_title = models.CharField(max_length=255)
    fare = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.route_title


class Hostel(models.Model):
    hostel_name = models.CharField(max_length=255)
    hostel_type = models.CharField(max_length=255, choices=[("select", "select"), ("Girls", "Girls"), ("Boys", "Boys"), ("Combine", "Combine")])
    address = models.CharField(max_length=255, blank=True, null=True)
    intake = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.hostel_name


class FeesGroup(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class FeesType(models.Model):
    name = models.CharField(max_length=250)
    Fees_code = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class Incomehead(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.name


class ExpenseHead(models.Model):
    expense_head = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.expense_head


class Role(models.Model):
    name = models.CharField(max_length=255)
    permissions = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class AddLeaveType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name





class Designation(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class AddItem(models.Model):
    item = models.CharField(max_length=255, unique=True)
    item_category = models.ForeignKey("sub_part.ItemCategory", on_delete=models.CASCADE)
    unit = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.item


class ItemCategory(models.Model):
    item_category = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.item_category


class ItemStore(models.Model):
    item_store_name = models.CharField(max_length=255)
    item_stock_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.item_store_name


class ItemSupplier(models.Model):
    name = models.CharField(max_length=255)
    phone_no = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    contact_person_name = models.CharField(max_length=255, blank=True, null=True)
    contact_person_phone = models.IntegerField(blank=True, null=True)
    contact_person_email = models.EmailField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class AdmissionEnquiry(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=13)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(max_length=250, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    assigned = models.CharField(max_length=50, blank=True, null=True)
    reference = models.ForeignKey(Reference, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    number_of_child = models.IntegerField(blank=True, null=True)


class VisitorBook(models.Model):
    purpose = models.ForeignKey(Purpose, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=500, blank=True, null=True)
    id_card = models.CharField(max_length=50, blank=True, null=True)
    number_of_person = models.IntegerField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)


class PhoneCallLog(models.Model):
    type = (("Incoming", "Incoming"), ("Outgoing", "Outgoing"))
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    call_duration = models.CharField(max_length=250, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    call_type = models.CharField(max_length=50, choices=type, default="Incoming")


class PostalDispatch(models.Model):
    to_title = models.CharField(max_length=50)
    reference_no = models.IntegerField()
    address = models.TextField(max_length=250, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)
    from_title = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)


class PostalReceive(models.Model):
    from_title = models.CharField(max_length=50)
    reference_no = models.IntegerField()
    address = models.TextField(max_length=250, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)
    to_title = models.CharField(max_length=50)
    date = models.DateField(blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)


class Complain(models.Model):
    complain_type = models.ForeignKey(ComplainType, on_delete=models.CASCADE)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    complain_by = models.CharField(max_length=50)
    phone = models.CharField(max_length=13)
    date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    action_taken = models.CharField(max_length=50, blank=True, null=True)
    assigned = models.CharField(max_length=50, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)

from datetime import date
class StudentAdmission(models.Model):
    admission_no = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100,blank=True, null=True)  
    Class = models.ForeignKey(Class, on_delete=models.CASCADE,blank=True, null=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,blank=True, null=True)
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500, blank=True, null=True)  
    gender = models.CharField(max_length=500, choices=(("Male", "Male"), ("Female", "Female")), blank=True, null=True)   
    date_of_birth = models.DateField()
    category = models.ForeignKey(
        StudentCategory, on_delete=models.CASCADE, blank=True, null=True
    )  
    religion = models.CharField(max_length=500, blank=True, null=True)  
    Caste = models.CharField(max_length=500, blank=True, null=True)  
    mobile_number = models.CharField(max_length=500, blank=True, null=True)  
    email = models.EmailField(max_length=500, blank=True, null=True)  
    admission_date = models.DateField(default=date.today, blank=True, null=True)
    student_photo = models.FileField(blank=True, null=True)
    Blood_group = models.CharField(max_length=100, choices=(("O+", "O+"), ("A+", "A+"), ("B+", "B+"), ("AB+", "AB+"), ("O-", "O-"), ("A-", "A-"), ("B-", "B-"), ("AB-", "AB-")), blank=True, null=True)  
    height = models.CharField(max_length=500, blank=True, null=True)  
    weight = models.CharField(max_length=500, blank=True, null=True)  
    as_on_date = models.DateField(blank=True, null=True)  
    bank_account_number = models.CharField(max_length=500, blank=True, null=True)  
    bank_name = models.CharField(max_length=500, blank=True, null=True)  
    ifsc_code = models.CharField(max_length=500, blank=True, null=True)  
    national_identification_number = models.CharField(
        max_length=50, blank=True, null=True
    )
    local_identification_number = models.CharField(max_length=50, blank=True, null=True)
    rte = models.CharField(max_length=100, choices=(("Yes", "Yes"), ("No", "No")), default="No")  
    previous_school_detail = models.TextField(max_length=250, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)

    title_1 = models.CharField(max_length=500, blank=True, null=True)
    documents_1 = models.FileField(blank=True, null=True)
    title_2 = models.CharField(max_length=500, blank=True, null=True)
    documents_2 = models.FileField(blank=True, null=True)
    title_3 = models.CharField(max_length=500, blank=True, null=True)
    documents_3 = models.FileField(blank=True, null=True)
    title_4 = models.CharField(max_length=500, blank=True, null=True)
    documents_4 = models.FileField(blank=True, null=True)

    disable_date = models.DateField(blank=True, null=True)
    diable_reson = models.ForeignKey(
        DisableReason, on_delete=models.CASCADE, blank=True, null=True
    )
    disable_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=250, default="Enable", blank=True, null=True)
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )
    user_student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_student",
    )
    user_parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="user_parent",
    )

      
    student_health = models.CharField(max_length=100, blank=True, null=True)    
    student_health_description	= models.TextField(max_length=550, blank=True, null=True)
    name_of_last_school = models.CharField(max_length=250,blank=True, null=True)
    leaving_last_school_reason = models.TextField(max_length=550,blank=True, null=True)
    grade_completed = models.CharField(max_length=100, choices=(("Yes", "Yes"), ("No", "No")), blank=True, null=True)  
    suspended_or_not = models.CharField(max_length=100, blank=True, null=True)
    is_suspension_resolved = models.CharField(max_length=100, blank=True, null=True) 
    suspension_reason = models.TextField(max_length=550,blank=True, null=True)
    county = models.CharField(max_length=250,blank=True, null=True)
    sub_county =  models.CharField(max_length=250,blank=True, null=True)
    ward = models.CharField(max_length=250,blank=True, null=True)
    source = models.CharField(max_length=250, default="offline",null=True, blank=True) 
    vehicle_number=models.ForeignKey('sub_part.vehicle',on_delete=models.CASCADE,blank=True,null=True)
    route_list=models.ForeignKey(Route,on_delete=models.CASCADE,blank=True,null=True)
    hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,blank=True,null=True)
    student_main=models.ForeignKey('sub_part.StudentMain',on_delete=models.CASCADE,blank=True,null=True)


    def get_or_generate_account_number(self):
        return f"SCH-{str(self.id)}"

    def get_school_account_number(self):
        
        return self.get_or_generate_account_number()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.id}"

class StudentGuardianDetails(models.Model): 
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE,)
    guardianmaster = models.ForeignKey(GuardianMaster, on_delete=models.CASCADE,)
    name=models.CharField(max_length=500) 
    phone=models.CharField(max_length=513)
    occupation=models.CharField(max_length=500)
    guardian_email=models.EmailField(blank=True, null=True)

class LoginCredentials(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    student_username = models.CharField(max_length=50, blank=True, null=True)
    student_password = models.CharField(max_length=50, blank=True, null=True)
    parent_username = models.CharField(max_length=50, blank=True, null=True)
    parent_passwod = models.CharField(max_length=50, blank=True, null=True)

class DisableHistroy(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    disable_date = models.DateField()
    diable_reson = models.ForeignKey(DisableReason, on_delete=models.CASCADE)
    disable_note = models.TextField()
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )

class AddIncome(models.Model):
    Income_head = models.ForeignKey(
        Incomehead, on_delete=models.CASCADE, blank=True, null=True
    )
    invoice_number = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    attach_document = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)


class IncomeExpense(models.Model):
    entry_type = models.CharField(max_length=10, choices=[("expense", "Expense"), ("income", "Income")])
    object_id = models.PositiveIntegerField()
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    attach_document = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.get_entry_type_display()} - {self.content_object}"
    class Meta:
        ordering = ["-date"]


class FeesCollectionAccount(models.Model):
    account_id = models.CharField(max_length=50)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    income_expense_head = models.ForeignKey(IncomeExpense, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)

    def __str__(self):
        return f"Fees Collection Account ID: {self.account_id}, Balance: {self.account_balance}"

    class Meta:
        ordering = ["-date_time"]


class ExpenseCashBookAccount(models.Model):
    account_type = models.CharField(max_length=10, choices=[("Income", "Income"), ("Expense", "Expense"), ("Cash", "Cash"), ("Book", "Book")])
    account_id = models.CharField(max_length=50)
    account_balance = models.DecimalField(max_digits=10, decimal_places=2)
    income_expense_head = models.ForeignKey(IncomeExpense, on_delete=models.CASCADE)
    income = models.ForeignKey("Account", on_delete=models.CASCADE)


    def __str__(self):
        return f"Expense Cash Book Account ID: {self.account_id}, Balance: {self.account_balance}"

    class Meta:
        ordering = ["-account_type"]


class FeesMaster(models.Model):
    fees_group = models.ForeignKey(FeesGroup, on_delete=models.CASCADE)
    fees_type = models.ForeignKey(FeesType, on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    amount = models.FloatField(max_length=50)
    fine_type = models.CharField(max_length=50, choices=[("Select", "Select"), ("Percentage", "Percentage"), ("Fine Amount", "Fine Amount")], blank=True, null=True)
    percentage = models.CharField(max_length=250)
    fine_amount = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=250, default="Active")

    def __str__(self):
        return str(self.amount)


class FeesAssign(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    fees = models.ForeignKey(FeesMaster, on_delete=models.CASCADE)
    balance_amount = models.IntegerField(blank=True, null=True)
    paid_amount = models.IntegerField(blank=True, null=True, default=0)
    Dicount_amount = models.IntegerField(blank=True, null=True, default=0)
    fine_amount = models.IntegerField(blank=True, null=True, default=0)
    status = models.CharField(max_length=100)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)



class DiscountAssign(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    discount = models.ForeignKey("sub_part.FeesTypeDiscount", on_delete=models.CASCADE)
    fees = models.ForeignKey(
        "sub_part.FeesAssign", on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.CharField(max_length=100)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)



class AddExpense(models.Model):
    expense_head = models.ForeignKey(ExpenseHead, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=255)
    date = models.DateTimeField()
    amount = models.IntegerField()
    attach_document = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)



class FeesTypeDiscount(models.Model):
    total_fees = models.ForeignKey(
        FeesMaster,
        on_delete=models.CASCADE,
        related_name="total_fees1",
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=250)
    discount_code = models.IntegerField()
    discount_type = models.CharField(max_length=50, choices=[("Discount Percentage", "Discount Percentage"), ("Discount Amount", "Discount Amount")], blank=True, null=True)
    amount = models.IntegerField(default=0)
    percentage = models.FloatField(default=0, blank=True, null=True)
    description = models.TextField(max_length=250, blank=True, null=True)
    percentage_amount = models.IntegerField(default=0)


    def save(self, *args, **kwargs):
        if self.discount_type == "Discount Percentage":
            if self.total_fees and self.percentage is not None:
                total_amount = self.total_fees.amount
                calculated_percentage_amount = (self.percentage / 100) * total_amount
                self.amount = calculated_percentage_amount
                self.percentage_amount = (
                    calculated_percentage_amount
                )
        super(FeesTypeDiscount, self).save(*args, **kwargs)

class AssetType(models.Model):
    assert_type_ID = models.IntegerField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=[("active", "Active"), ("inactive", "Inactive")])
    asset_category = models.CharField(max_length=100, choices=[("Asset", "Asset"), ("Liability", "Liability"), ("Income", "Income"), ("Expenses", "Expenses")])


    def _str_(self):
        return str(self.short_description)

class ChargeType(models.Model):
    charge_type_ID = models.CharField(
        max_length=100, primary_key=True, null=False, blank=False
    )
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    mode = models.CharField(max_length=100, choices=[("flat", "Flat Charge"), ("percentage", "Percentage")], default="percentage")
    value = models.FloatField(default=100)
    Dr_charge_GL_category = models.CharField(max_length=100, default="NA")
    Cr_charge_GL_category = models.CharField(max_length=100, default="NA")
    


    def _str_(self):
        return self.short_description

class GLLine(models.Model):
    line_number = models.IntegerField(primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    
    assert_type_ID = models.ForeignKey(
        AssetType, on_delete=models.CASCADE, null=True, blank=True
    )
    master_GL_line = models.ForeignKey(
        "GLLine", on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.CharField(max_length=100, choices=[("active", "Active"), ("inactive", "Inactive")])
    current_cleared_balance = models.FloatField(default=0)
    current_uncleared_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)


    def __str__(self):
        return str(self.line_number)

    @classmethod
    def get_school_gl_line(cls):
        try:
            return cls.objects.get(short_description="School GL Line", status="active")
        except cls.DoesNotExist:
            print("GLLine for schools not found.")
        except Exception as error:
            print(f"Error while getting GLLine for schools: {error}")
        return None

    @classmethod
    def create_school_gl_line(cls):
        try:
            return cls.objects.create(
                short_description="School GL Line",
                description="GL Line for schools",
                status="active",
                current_cleared_balance=0,
                current_uncleared_balance=0,
                total_balance=0,
            )
        except Exception as error:
            print(f"Error while getting GLLine for schools: {error}")
        return None


class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False, null=False)
    abbreviation = models.CharField(max_length=10, null=True, unique=True, blank=False)
    description = models.CharField(max_length=250, unique=True, blank=True, null=True)


    def __str__(self):
        return self.name


class Account(models.Model):
    account_type = models.ForeignKey(
        AccountType, null=True, blank=True, on_delete=models.CASCADE
    )
    gl_line_number = models.ForeignKey(
        GLLine,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="gl_line_number",
    )
    account_number = models.CharField(max_length=50, null=True, blank=True)
    account_description = models.CharField(
        max_length=100, null=True, blank=True, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    opening_balance = models.FloatField(default=0)
    current_cleared_balance = models.FloatField(default=0)
    current_uncleared_balance = models.FloatField(default=0)
    total_balance = models.FloatField(default=0)


    def __str__(self):
        return self.account_number


class TransactionCode(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    short_description = models.CharField(max_length=100, unique=True)
    description = models.TextField()
   


    def __str__(self):
        return self.short_description


class TransactionType(models.Model):
    type_id = models.CharField(max_length=10, primary_key=True, default="txn-001")
    short_description = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    dr_transaction_code = models.ForeignKey(
        TransactionCode,
        on_delete=models.CASCADE,
        related_name="dr_txn_code",
        null=True,
        blank=True,
    )
    dr_gl = models.ForeignKey(
        GLLine, on_delete=models.CASCADE, related_name="dr_gl", null=True, blank=True
    )
    dr_acc = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="dr_acc", null=True, blank=True
    )
    cr_transaction_code = models.ForeignKey(
        TransactionCode,
        on_delete=models.CASCADE,
        related_name="cr_txn_code",
        null=True,
        blank=True,
    )
    cr_gl = models.ForeignKey(
        GLLine, on_delete=models.CASCADE, related_name="cr_gl", null=True, blank=True
    )
    cr_acc = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="cr_acc", null=True, blank=True
    )
    fee1_mode = models.CharField(max_length=10, choices=(("percentage", "percentage"), ("flat", "flat")), default="percentage")
    fee1 = models.FloatField(default=0)
    fee2_mode = models.CharField(max_length=10, choices=(("percentage", "percentage"), ("flat", "flat")), default="percentage")
    fee2 = models.FloatField(default=0)
    fee3_mode =models.CharField(max_length=10, choices=(("percentage", "percentage"), ("flat", "flat")), default="percentage")
    fee3 = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=[("active", "Active"), ("inactive", "Inactive")], default="active")
    is_income = models.BooleanField(default=False)
    is_expense = models.BooleanField(default=False)


    def __str__(self):
        return self.short_description


class AccountEntry(models.Model):
    entry_ID = models.CharField(max_length=50, unique=True, blank=False, null=False)
    entry_type = models.CharField(max_length=2, choices=(("PL", "PL"), ("AL", "AL")), null=True, blank=True)
    transaction_ID = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user", null=True, blank=True
    )

    student_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="student_account_entries",
        null=True,
        blank=True,
    )
    school_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="school_account_entries",
        null=True,
        blank=True,
    )

    amount = models.FloatField()
    currency = models.CharField(max_length=10, default="KES")
    debit_credit_marker = models.CharField(max_length=100)
    exposure_date = models.DateTimeField(auto_now_add=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    posting_date = models.DateTimeField(default=timezone.now)  
 
    transaction_type = models.ForeignKey(
        TransactionType, on_delete=models.CASCADE, null=True, blank=True
    )


    def __str__(self):
        return str(self.transaction_ID)
    
    @property
    def is_income(self):
        return self.transaction_type == 'income'

    @property
    def is_expense(self):
        return self.transaction_type == 'expense'


class FinancialTransaction(models.Model):
    transaction_type = models.ForeignKey("TransactionType", on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.TextField()



class JournalEntry(models.Model):
    transaction = models.ForeignKey(FinancialTransaction, on_delete=models.CASCADE)
    gl_line = models.ForeignKey("GLLine", on_delete=models.CASCADE)
    debit_amount = models.FloatField()
    credit_amount = models.FloatField()


class Addleave(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    apply_date = models.DateField()
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField(max_length=255, blank=True, null=True)
    attach_document = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=100, default="disapprove",blank=True, null=True)
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )

    approved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="approved_by",
    )


class ExamType(models.Model):   
    name = models.CharField(max_length=355 )
    description = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.name

class examGroup(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class AdmitCard(models.Model):
    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    template = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    exam_name = models.CharField(max_length=255, blank=True, null=True)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    exam_center = models.CharField(max_length=255, blank=True, null=True)
    footer_text = models.CharField(max_length=255, blank=True, null=True)
    left_logo = models.FileField(blank=True, null=True)
    right_logo = models.FileField(blank=True, null=True)
    sign = models.FileField(blank=True, null=True)
    background_image = models.FileField(blank=True, null=True)
    name = models.BooleanField(choices=BOOL_CHOICES)
    father_name = models.BooleanField(choices=BOOL_CHOICES)
    mother_name = models.BooleanField(choices=BOOL_CHOICES)
    date_of_birth = models.BooleanField(choices=BOOL_CHOICES)
    admission_no = models.BooleanField(choices=BOOL_CHOICES)
    roll_no = models.BooleanField(choices=BOOL_CHOICES)
    address = models.BooleanField(choices=BOOL_CHOICES)
    gender = models.BooleanField(choices=BOOL_CHOICES)
    photo = models.BooleanField(choices=BOOL_CHOICES)
    Class = models.BooleanField(choices=BOOL_CHOICES)
    section = models.BooleanField(choices=BOOL_CHOICES)


class DesignMarkSheet(models.Model):
    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    template = models.CharField(max_length=255)
    heading = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    exam_name = models.CharField(max_length=255, blank=True, null=True)
    school_name = models.CharField(max_length=255, blank=True, null=True)
    exam_center = models.CharField(max_length=255, blank=True, null=True)
    body_text = models.TextField(max_length=255, blank=True, null=True)
    footer_text = models.TextField(max_length=255, blank=True, null=True)
    printing_date = models.DateField(blank=True, null=True)
    left_logo = models.FileField(blank=True, null=True)
    right_logo = models.FileField(max_length=255, blank=True, null=True)
    left_sign = models.FileField(max_length=255, blank=True, null=True)
    middle_sign = models.FileField(max_length=255, blank=True, null=True)
    right_sign = models.FileField(max_length=255, blank=True, null=True)
    background_image = models.FileField(max_length=255, blank=True, null=True)
    name = models.BooleanField(choices=BOOL_CHOICES)
    father_name = models.BooleanField(choices=BOOL_CHOICES)
    mother_name = models.BooleanField(choices=BOOL_CHOICES)
    date_of_birth = models.BooleanField(choices=BOOL_CHOICES)
    admission_no = models.BooleanField(choices=BOOL_CHOICES)
    roll_no = models.BooleanField(choices=BOOL_CHOICES)
    address = models.BooleanField(choices=BOOL_CHOICES)
    gender = models.BooleanField(choices=BOOL_CHOICES)
    photo = models.BooleanField(choices=BOOL_CHOICES)
    grade = models.BooleanField(choices=BOOL_CHOICES)
    section = models.BooleanField(choices=BOOL_CHOICES)


class AddGrade(models.Model):
    exam_type = models.ForeignKey(ExamType, on_delete=models.CASCADE, null=True, blank=True)
    grade_name = models.CharField(max_length=255)
    percent_up_to = models.FloatField()
    percent_from = models.FloatField()
    grade_point = models.FloatField()
    description = models.TextField(max_length=255, blank=True, null=True)



class OnlineExam(models.Model):
    exam_title = models.CharField(max_length=255)
    exam_from = models.DateField()
    exam_to = models.DateField()
    time_duration = models.DurationField(blank=True, null=True)
    attempt = models.IntegerField(blank=True, null=True)
    passing_percentage = models.IntegerField(blank=True, null=True)
    publish = models.BooleanField(blank=True, null=True)
    publish_result = models.BooleanField(blank=True, null=True)
    description = models.TextField(max_length=255)


class QuestionBank(models.Model):
    subject = models.CharField(max_length=255)
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)


class Lesson(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject_group = models.ForeignKey("sub_part.SubjectGroup", on_delete=models.CASCADE)
    subject = models.ForeignKey("sub_part.Subjects", on_delete=models.CASCADE)
    lesson_name = models.CharField(max_length=255)


class topic(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    subject_group = models.ForeignKey("sub_part.SubjectGroup", on_delete=models.CASCADE)
    subject = models.ForeignKey("sub_part.Subjects", on_delete=models.CASCADE)
    lesson_name = models.ForeignKey("sub_part.Lesson", on_delete=models.CASCADE)
    topic_name = models.CharField(max_length=255)
    date_save = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=15, blank=True, null=True)



class AssignClassTeacher(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )
    class_teacher = models.ManyToManyField("sub_part.AddStaff")


class AssignSubjectTeacher(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )
    class_teacher = models.ForeignKey(
        ("sub_part.AddStaff"), on_delete=models.CASCADE, blank=True, null=True
    )
    subject = models.ManyToManyField("Subjects")


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)
    subject_type = models.CharField(max_length=20, choices=[("theory", "Theory"), ("practical", "Practical")], blank=True, null=True)
    subject_code = models.CharField(max_length=15, blank=True, null=True)
    grading = models.ForeignKey(
        GradingSystem, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.subject_name


class SubjectGroup(models.Model):
    name = models.CharField(max_length=255)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject = models.ManyToManyField(Subjects)
    description = models.TextField(max_length=255)

    def __str__(self):
        return self.name


class Curriculum(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    curriculum_type = models.CharField(max_length=10, choices=[("CBC", "CBC"), ("8.4.4", "8.4.4"), ("IGCSE", "IGCSE"), ("IB", "IB"), ("A.C.E", "Accelerated Christian Education")], default="")


class ApproveLeave(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    name = models.ForeignKey("sub_part.Addstaff", on_delete=models.CASCADE)
    apply_date = models.DateField()
    leave_type = models.ForeignKey(AddLeaveType, on_delete=models.CASCADE)
    leave_dates = models.TextField()
    number_of_days = models.IntegerField(blank=True, null=True)
    LOP_leave_dates = models.TextField(blank=True, null=True)
    LOP_number_of_days = models.IntegerField(blank=True, null=True)
    reason = models.TextField(max_length=255, blank=True, null=True)
    note = models.TextField(max_length=255, blank=True, null=True)
    attach_document = models.FileField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=[("Pending", "Pending"), ("Approve", "Approve"), ("Disapprove", "Disapprove")], default="Pending")



class ApplyLeave(models.Model):
    apply_date = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=255, choices=[("Select", "Select"), ("admin", "admin")])
    leave_date_from = models.DateField()
    leave_date_to = models.DateField()
    reason = models.TextField(max_length=255)
    attach_document = models.FileField(blank=True, null=True)

class noticeBoard(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField(max_length=255)
    notice_date = models.DateField()
    publish_on = models.DateField()
    message_to = models.CharField(max_length=255)

class UploadContent(models.Model):
    content_title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=[("assignments", "Assignments"), ("study_material", "Study Material"), ("syllabus", "Syllabus"), ("other_download", "Other Download")])
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    upload_date = models.DateField()
    description = models.TextField()
    file = models.FileField()


class AddHomeWork(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    homework_date = models.DateField()
    submission_date = models.DateField()
    attach_document = models.FileField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    evaluation_date = models.DateField(blank=True, null=True)



class AddBook(models.Model):
    book_title = models.CharField(max_length=255)
    book_number = models.CharField(max_length=255, blank=True, null=True)
    ISBN_number = models.CharField(max_length=255, blank=True, null=True)
    publisher = models.CharField(max_length=255, blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    rank_number = models.CharField(max_length=255, blank=True, null=True)
    qty = models.IntegerField()
    available_qty = models.IntegerField()
    book_price = models.IntegerField()
    post_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.book_title


class IssueBook(models.Model):
    book = models.ForeignKey("sub_part.AddBook", on_delete=models.CASCADE)
    member = models.ForeignKey("sub_part.LibrayMember", on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_return_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)


class LibrayMember(models.Model):
    library_card_no = models.CharField(max_length=255)
    staff = models.ForeignKey(
        "sub_part.AddStaff", on_delete=models.CASCADE, blank=True, null=True
    )
    student = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )
    member_type = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="active")



class IssueItem(models.Model):
    user_type = models.ForeignKey(Role, on_delete=models.CASCADE)
    issued_to = models.ForeignKey(
        "sub_part.AddStaff", on_delete=models.CASCADE, related_name="issue_to"
    )
    issued_by = models.ForeignKey("sub_part.AddStaff", on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, default="issued", blank=True, null=True)
    quantity = models.IntegerField()


class NonReturnableItem(models.Model):
    user_type = models.ForeignKey(Role, on_delete=models.CASCADE)
    staff = models.ForeignKey(
        "sub_part.AddStaff", on_delete=models.CASCADE, related_name="issue_to1"
    )
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)
    inventory_id = models.CharField(max_length=255)
    min_quantity = models.IntegerField()
    max_quantity = models.IntegerField()
    duration_in_days = models.PositiveIntegerField()


class ItemReturn(models.Model):
    return_date = models.DateField()
    remark = models.TextField(blank=True, null=True)
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class ItemStock(models.Model):
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)
    supplier = models.ForeignKey(ItemSupplier, on_delete=models.CASCADE)
    store = models.ForeignKey(ItemStore, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.IntegerField()
    date = models.DateField()
    attach_document = models.FileField(blank=True, null=True)
    description = models.TextField(max_length=255, blank=True, null=True)


class ItemStockDeatail(models.Model):
    item_category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    item = models.ForeignKey(AddItem, on_delete=models.CASCADE)
    supplier = models.ForeignKey(ItemSupplier, on_delete=models.CASCADE)
    store = models.ForeignKey(ItemStore, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    available_quantity = models.IntegerField(blank=True, null=True)



class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255, blank=True, null=True)
    year_made = models.PositiveIntegerField(blank=True, null=True)
    driver_name = models.CharField(max_length=255, blank=True, null=True)
    driver_licence = models.CharField(max_length=255, blank=True, null=True)
    driver_contact = models.IntegerField(blank=True, null=True)
    note = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.vehicle_number


class AssignVehicle(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, blank=True, null=True)
    vehicle = models.ManyToManyField(Vehicle)


class HostelRoom(models.Model):
    room_name = models.CharField(max_length=255)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    room_type = models.ForeignKey("sub_part.RoomType", on_delete=models.CASCADE)
    number_of_bed = models.IntegerField()
    cost_per_bed = models.IntegerField()
    description = models.TextField(max_length=255, blank=True, null=True)


class RoomType(models.Model):
    room_type = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True, null=True)
    def __str__(self):
        return self.room_type


class StudentCertificate(models.Model):
    certificate_name = models.CharField(max_length=255, blank=True, null=True)
    header_left_text = models.CharField(max_length=500, blank=True, null=True)
    header_center_text = models.CharField(max_length=255, blank=True, null=True)
    header_right_text = models.CharField(max_length=700, blank=True, null=True)
    body_text = models.TextField(max_length=5000, blank=True, null=True)
    footer_left_text = models.CharField(max_length=255, blank=True, null=True)
    footer_center_text = models.CharField(max_length=255, blank=True, null=True)
    footer_right_text = models.CharField(max_length=255, blank=True, null=True)
    background_image = models.FileField(blank=True, null=True)
    student_image = models.FileField(blank=True, null=True)
    background_color_code = models.CharField(max_length=255, blank=True, null=True)


class StudentId(models.Model):
    BOOL_CHOICES = ((True, "Yes"), (False, "No"))
    background_image = models.FileField(blank=True, null=True)
    logo = models.FileField(blank=True, null=True)
    signature = models.FileField(blank=True, null=True)
    school_name = models.CharField(max_length=255)
    address = models.TextField(max_length=255)
    id_card_title = models.CharField(max_length=255)
    header_color = models.CharField(max_length=255)
    admission_no = models.BooleanField(choices=BOOL_CHOICES)
    student_name = models.BooleanField(choices=BOOL_CHOICES)
    Class = models.BooleanField(choices=BOOL_CHOICES)
    father_name = models.BooleanField(choices=BOOL_CHOICES)
    mother_name = models.BooleanField(choices=BOOL_CHOICES)
    student_address = models.BooleanField(choices=BOOL_CHOICES)
    phone = models.BooleanField(choices=BOOL_CHOICES)
    date_of_birth = models.BooleanField(choices=BOOL_CHOICES)
    blood_group = models.BooleanField(choices=BOOL_CHOICES)



class Event(models.Model):
    event_title = models.CharField(max_length=255)
    venue = models.CharField(max_length=255, null=True, blank=True)
    event_start = models.DateField()
    event_end = models.DateField()
    sidebar = models.BooleanField(blank=True, null=True)
    add_media = models.FileField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255)
    meta_keyword = models.CharField(max_length=255)
    meta_description = models.CharField(max_length=255)


class MediaManager(models.Model):
    file = models.FileField(blank=True, null=True)
    url = models.URLField()


class Menu(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)


class Session(models.Model):
    session = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.session) if self.session is not None else ""


class AlumniEvent(models.Model):
    event_for = models.CharField(max_length=20, choices=[("all_alumini", "All Alumni"), ("Class", "Class")])
    passed_out_session = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    select_class = models.ForeignKey(
        Class, on_delete=models.CASCADE, blank=True, null=True
    )
    section = models.ManyToManyField(Section, blank=True)
    event_title = models.CharField(max_length=255)
    event_date_from = models.DateField()
    event_date_to = models.DateField()
    note = models.TextField(blank=True, null=True)
    event_notification_message = models.TextField(blank=True, null=True)
    email = models.BooleanField()
    sms = models.BooleanField()


class AddStaff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    staff_id = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=25)
    roles = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True)
    designation = models.ForeignKey(
        Designation,
        on_delete=models.CASCADE,
        related_name="designation_staff_directory",
        blank=True,
        null=True,
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="department_staff_directory",
        blank=True,
        null=True,
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    gender = models.CharField(max_length=100, choices=[("female", "Female"), ("male", "Male")])
    date_of_birth = models.DateField(blank=True, null=True)
    date_of_joining = models.DateField(blank=True, null=True)
    phone_no = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    marital_status = models.CharField(max_length=20, blank=True, null=True, choices=[("single", "Single"), ("married", "Married"), ("widowed", "Widowed"), ("separated", "Separated"), ("not_specified", "Not Specified")])
    photo = models.FileField(blank=True, null=True)
    current_address = models.TextField(max_length=255, blank=True, null=True)
    permanent_address = models.TextField(max_length=255, blank=True, null=True)
    qualification = models.TextField(max_length=255, blank=True, null=True)
    work_experience = models.TextField(max_length=255, blank=True, null=True)
    note = models.TextField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100, default="Enable", blank=True, null=True)
    disable_date = models.DateField(blank=True, null=True)
 
    
    nssf_no = models.CharField(max_length=255, blank=True, null=True)
    shif_no = models.CharField(max_length=255, blank=True, null=True)
    phone_no = models.CharField(max_length=255, blank=True, null=True)
    basic_salary = models.CharField(max_length=255, blank=True, null=True)
    contract_type = models.CharField(max_length=20, blank=True, null=True, choices=[("probation", "Probation"), ("permanent", "Permanent")])
    work_shift = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    bank_title = models.CharField(max_length=255, blank=True, null=True)
    account_no = models.CharField(max_length=255, blank=True, null=True)
    ifsc_code = models.CharField(max_length=255, blank=True, null=True)
    branch_name = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
 
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
  
    
    title_1 = models.CharField(max_length=500, blank=True, null=True)
    documents_1 = models.FileField(blank=True, null=True)
    title_2 = models.CharField(max_length=500, blank=True, null=True)
    documents_2 = models.FileField(blank=True, null=True)
    title_3 = models.CharField(max_length=500, blank=True, null=True)
    documents_3 = models.FileField(blank=True, null=True)
    title_4 = models.CharField(max_length=500, blank=True, null=True)
    documents_4 = models.FileField(blank=True, null=True)
    school = models.ForeignKey(
        "sub_part.SchoolRegistration",
        on_delete=models.CASCADE,
        related_name="AddStaff_school",
        
    )
    is_admin = models.BooleanField(default=False)
    

    def __str__(self):
        return self.first_name + " (" + self.staff_id + ") "
    
class StaffEducationQualification(models.Model): 
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE,)
    staff_school = models.CharField(max_length=500)
    degree = models.CharField(max_length=500)
    study=models.CharField(max_length=500) 
    start_date=models.DateField(max_length=513) 
    end_date=models.DateField(max_length=513) 
    grade=models.CharField(max_length=513)
    

class StaffLeave(models.Model):
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(AddLeaveType, on_delete=models.CASCADE)
    total_leave = models.IntegerField()


class AvailableLeave(models.Model):
    staff_leave = models.ForeignKey(StaffLeave, on_delete=models.CASCADE)
    available_leave = models.IntegerField()
    total_leave = models.IntegerField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)


class Timeline(models.Model):
    student = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=250)
    date = models.DateField()
    description = models.TextField(max_length=500, blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)
    visible_to_this_person = models.BooleanField(default=False)
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )



class StudentFess(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    paid_amount = models.CharField(max_length=100, blank=True, null=True)
    discount_group = models.ForeignKey(
        DiscountAssign, on_delete=models.CASCADE, blank=True, null=True
    )
    fess = models.ForeignKey(
        FeesAssign, on_delete=models.CASCADE, blank=True, null=True
    )
    payment_mode_fee = models.CharField(max_length=100, blank=True, null=True)
    amount_discount = models.CharField(max_length=100, blank=True, null=True)
    amount_fine = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    paid_by = models.CharField(max_length=500, blank=True, null=True)
    ref_number = models.CharField(max_length=500, blank=True, null=True)
    card_holder_name = models.CharField(max_length=1500, blank=True, null=True)
    mobile_number = models.IntegerField(blank=True, null=True)
    amount =  models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    status = models.CharField(max_length=100)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)




class PaymentRecord(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    paid_amount = models.CharField(max_length=100, blank=True, null=True)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)

    def __str__(self):
        return f"Cumulative Total Amount: {self.paid_amount}"


class StudentAttendance(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=100)
    attendance_date = models.DateField()
    note = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)


class PromoteStudent(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    currrent_result = models.CharField(max_length=100, blank=True, null=True)
    next_session_status = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)


class TimeTable(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    subject_group = models.ForeignKey(SubjectGroup, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    teacher = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    time_from = models.TimeField()
    time_to = models.TimeField()
    room_no = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)


class AddExam(models.Model):
    exam_group = models.ForeignKey(
        examGroup, on_delete=models.CASCADE, blank=True, null=True
    )
    Exam = models.CharField(max_length=100)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, blank=True, null=True
    )
    publish = models.BooleanField()
    publish_result = models.BooleanField()
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.Exam


class ExamStudent(models.Model):
    exam = models.ForeignKey("sub_part.AddExam", on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class AddExamSubject(models.Model):
    exam = models.ForeignKey("sub_part.AddExam", on_delete=models.CASCADE)
    subject = models.ForeignKey("sub_part.Subjects", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True)
    credit_hours = models.CharField(max_length=100, blank=True, null=True)
    room_number = models.CharField(max_length=100, blank=True, null=True)
    marks_max = models.FloatField(max_length=100, blank=True, null=True)
    marks_min = models.FloatField(max_length=100, blank=True, null=True)


class EntryMarks(models.Model):
    exam = models.ForeignKey("sub_part.AddExam", on_delete=models.CASCADE)
    exam_student = models.ForeignKey(
        ExamStudent, on_delete=models.CASCADE, blank=True, null=True
    )
    exam_subject = models.ForeignKey(
        "sub_part.AddExamSubject", on_delete=models.CASCADE
    )
    subject = models.ForeignKey("sub_part.Subjects", on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    attendance = models.BooleanField()
    marks = models.IntegerField()
    note = models.CharField(max_length=100, blank=True, null=True)


class MarkDocument(models.Model):
    exam = models.ForeignKey("sub_part.AddExam", on_delete=models.CASCADE)
    subject = models.ForeignKey("sub_part.Subjects", on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    document = models.FileField(upload_to="Result Document/")


class StaffAttendance(models.Model):
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=100)
    attendance_date = models.DateField()
    note = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)


class PayrollSummary(models.Model):
    basic_salary = models.IntegerField(blank=False, null=True)
    earning = models.FloatField(blank=False, null=True)
    deduction = models.FloatField(blank=False, null=True)
    gross_salary = models.FloatField(blank=False, null=True)
    Tax = models.FloatField(blank=False, null=True)
    net_salary = models.FloatField(blank=False, null=True)
    Frist_name = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    payment_date = models.DateField(max_length=100, blank=False, null=True)
    Months = models.CharField(max_length=100, blank=False, null=True)
    year = models.CharField(max_length=100, blank=False, null=True)
    Payment_mode = models.CharField(max_length=100, blank=False, null=True)
    Note = models.TextField(max_length=500, blank=False, null=True)


class Managealumini(models.Model):
    Current_phone = models.IntegerField(blank=False, null=True)
    current_email = models.EmailField(blank=False, null=True)
    Occupation = models.CharField(max_length=200, blank=False, null=True)
    address = models.CharField(max_length=200, blank=False, null=True)
    photo = models.FileField(blank=False, null=True)
    students_id = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )


class GeneralSetting(models.Model):
    school_name = models.CharField(max_length=200)
    school_code = models.IntegerField()
    address = models.CharField(max_length=200)
    phone = models.IntegerField()
    email = models.EmailField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    months = models.CharField(max_length=100, choices=[("January", "january"), ("February", "february"), ("March", "march"), ("April", "april"), ("May", "may"), ("June", "june"), ("July", "July"), ("August", "august"), ("September", "september"), ("October", "october"), ("November", "november"), ("December", "december")], blank=True, null=True)
    country = models.CharField(max_length=100, choices=[("India", "India"), ("Kenya", "Kenya")], blank=True, null=True)

    edit_print_logo = models.ImageField(blank=True, null=True)
    edit_admin_logo = models.ImageField(blank=True, null=True)
    edit_admin_small_logo = models.ImageField(blank=True, null=True)

class StudentSession(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True, null=True)


class StudentClass(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True, null=True)


class AssingHomeWork(models.Model):
    home_work = models.ForeignKey(AddHomeWork, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    evaluation_date = models.DateField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    document = models.FileField(upload_to="Home work/", blank=True, null=True)
    status = models.CharField(max_length=100, blank=True, null=True)


class BasicWebPageDetails(models.Model):
    top_title = models.CharField(max_length=100, blank=True, null=True)
    first_title = models.CharField(max_length=100, blank=True, null=True)
    last_title = models.CharField(max_length=100, blank=True, null=True)
    school_address = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    about_us_title = models.CharField(max_length=100, blank=True, null=True)
    about_us_description = models.TextField(max_length=400, blank=True, null=True)
    about_us_image = models.FileField(blank=True, null=True)
    twitter_link = models.CharField(max_length=200, blank=True, null=True)
    facebook_link = models.CharField(max_length=200, blank=True, null=True)
    linkedIn_link = models.CharField(max_length=200, blank=True, null=True)
    Instagram_link = models.CharField(max_length=200, blank=True, null=True)


class CaroselImage(models.Model):
    carosel_image = models.FileField(upload_to="carosel_image/", blank=True, null=True)
    image_title = models.CharField(max_length=100, blank=True, null=True)
    image_description = models.CharField(max_length=100, blank=True, null=True)


class SchoolHeads(models.Model):
    head_name = models.CharField(max_length=100, blank=True, null=True)
    head_position = models.CharField(max_length=100, blank=True, null=True)
    head_image = models.FileField(blank=True, null=True)
    quotes = models.CharField(max_length=100, blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    linkedIn_link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.head_name


class SchoolStaff(models.Model):
    staff_name = models.CharField(max_length=100, blank=True, null=True)
    staff_position = models.CharField(max_length=100, blank=True, null=True)
    staff_image = models.FileField(blank=True, null=True)
    twitter_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    linkedIn_link = models.CharField(max_length=100, blank=True, null=True)


class Events(models.Model):
    event_title = models.CharField(max_length=100, blank=True, null=True)
    event_start_date = models.DateField(blank=True, null=True)
    event_end_date = models.DateField(blank=True, null=True)
    venue = models.CharField(max_length=255, null=True, blank=True)
    Approx_participants = models.IntegerField(blank=True, null=True)
    visual_media = models.FileField(blank=True, null=True)


class Infrastructure(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    total_count = models.CharField(max_length=100, blank=True, null=True)
    visual_media = models.FileField(blank=True, null=True)


class News(models.Model):
    news_title = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    visual_link = models.CharField(max_length=100, blank=True, null=True)
    visual_media = models.FileField(blank=True, null=True)


class Offers(models.Model):
    short_title = models.CharField(max_length=100, blank=True, null=True)
    Offer_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(max_length=700, blank=True, null=True)
    note1 = models.CharField(max_length=100, blank=True, null=True)
    note2 = models.CharField(max_length=100, blank=True, null=True)
    note3 = models.CharField(max_length=100, blank=True, null=True)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()


class WebEnquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    description = models.TextField()




class TeacherRating(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    assign_teacher = models.ForeignKey(AssignClassTeacher, on_delete=models.CASCADE)
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    status = models.CharField(max_length=100, default="pending")


class SendEmail(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    recipients = models.CharField(max_length=255)
    attachment = models.FileField(blank=True, null=True)


class LessonPlan(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    topic = models.ForeignKey(topic, on_delete=models.CASCADE)
    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE)
    sub_topic = models.CharField(max_length=100)
    lecture_youtube_url = models.URLField(blank=True, null=True)
    lecture_vedio = models.FileField(upload_to="lecture_vedio/", blank=True, null=True)
    attachment = models.FileField(
        upload_to="lecture_attachment/", blank=True, null=True
    )
    teaching_method = models.TextField(blank=True, null=True)
    general_objectives = models.TextField(blank=True, null=True)
    pervious_knowledge = models.TextField(blank=True, null=True)
    comprehensive_questions = models.TextField(blank=True, null=True)
    presentation = models.TextField(blank=True, null=True)
    date = models.DateField(blank=True, null=True)
  


class MailSearchTemp(models.Model):
    Staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE, blank=True, null=True)
    Student = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )
    Parent= models.ForeignKey(
        StudentGuardianDetails, on_delete=models.CASCADE, blank=True, null=True
    )
    type = models.CharField(max_length=100)

class MeetingLinkMaster(models.Model):
    link_for = models.CharField(max_length=250)
    type_of_application = models.CharField(max_length=100, choices=[("GoogleMeet", "Google Meet"), ("Zoom", "Zoom"), ("MicrosoftTeams", "Microsoft Teams"), ("Webex", "Webex"), ("ZohoMeeting", "Zoho Meeting"), ("Skype", "Skype"), ("TeamViewer", "TeamViewer"), ("GoToMeeting", "GoTo Meeting")])
    link= models.CharField(max_length=500)
    status = models.CharField(max_length=50, choices=[("Active", "Active"), ("Inactive", "Inactive")], default="Active")
    description = models.TextField(max_length=700, blank=True, null=True)
    

class OnlineClass(models.Model):
    class_title = models.CharField(max_length=250)
    class_date_time = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    staff = models.ForeignKey("sub_part.Addstaff", on_delete=models.CASCADE)
 
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ManyToManyField(Section)
    meeting_link = models.ForeignKey(MeetingLinkMaster, on_delete=models.CASCADE,blank=True, null=True)
    meeting_url = models.CharField(max_length=250,blank=True, null=True)
    description = models.TextField(max_length=700, blank=True, null=True)
    status = models.CharField(max_length=255, choices=[("Awaited", "Awaited"), ("Cancelled!", "Cancelled!"), ("Finished", "Finished")], default="Awaited")
    meeting_document = models.FileField(blank=True, null=True)
    meeting_notes = models.TextField(blank=True, null=True)


class StaffMeeting(models.Model):
    meeting_title = models.CharField(max_length=250)
    meeting_date_time = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_document = models.FileField(blank=True, null=True)
    meeting_notes = models.TextField(blank=True, null=True)
    staff = models.ManyToManyField("sub_part.Addstaff")
    meeting_url = models.CharField(max_length=250)
    description = models.TextField(max_length=700, blank=True, null=True)
    status = models.CharField(max_length=255, choices=[("Awaited", "Awaited"), ("Cancelled!", "Cancelled!"), ("Finished", "Finished")], default="Awaited")


class ParentMeeting(models.Model):
    meeting_title = models.CharField(max_length=250)
    meeting_date_time = models.DateTimeField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    meeting_document = models.FileField(blank=True, null=True)
    meeting_notes = models.TextField(blank=True, null=True)
    staff = models.ManyToManyField("sub_part.Addstaff")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, blank=True, null=True)
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, blank=True, null=True
    )
    student = models.ManyToManyField("sub_part.StudentAdmission")
    meeting_url = models.CharField(max_length=250)
    description = models.TextField(max_length=700, blank=True, null=True)
    status = models.CharField(max_length=255, choices=[("Awaited", "Awaited"), ("Cancelled!", "Cancelled!"), ("Finished", "Finished")], default="Awaited")


class StaffMeetingNote(models.Model):
    Staff_meeting = models.ForeignKey(
        StaffMeeting, on_delete=models.CASCADE, blank=True, null=True
    )
    note = models.TextField()
  


class ParentMeetingNote(models.Model):
    parent_meeting = models.ForeignKey(
        ParentMeeting, on_delete=models.CASCADE, blank=True, null=True
    )
    note = models.TextField()
  


class Studentmeetingnote(models.Model):
    student_meeting = models.ForeignKey(
        OnlineClass, on_delete=models.CASCADE, blank=True, null=True
    )
    note = models.TextField()



class EmailSetting(models.Model):
    gmail = models.CharField(max_length=200, blank=True, null=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    default_from_email = models.CharField(max_length=200, blank=True, null=True)
    email_port = models.CharField(max_length=200, blank=True, null=True)
    email_host = models.CharField(max_length=200, blank=True, null=True)


class AddContact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE, blank=True, null=True)
    contact_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="AddContact_contact_user"
    )
    usertype = models.CharField(max_length=100)


class ContanctMessage(models.Model):
    contact = models.ForeignKey(AddContact, on_delete=models.CASCADE)
    from_message = models.TextField(blank=True, null=True)
    to_message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200)


class SMSSetting(models.Model):
    twilio_account_SID = models.CharField(max_length=500, blank=True, null=True)
    twilio_auth_token = models.CharField(max_length=500, blank=True, null=True)
    twilio_regeister_phone_no = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)


class EmailSmsLog(models.Model):
    Title = models.CharField(max_length=200, blank=True, null=True)
    send_by = models.CharField(max_length=100)
    sent_to = models.CharField(max_length=100)



class EventCalendar(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    startstime = models.DateTimeField()
    endtime = models.DateTimeField()
    status = models.CharField(max_length=200, blank=True, null=True)
    repeats = models.CharField(max_length=500, choices=[("Public", "Public"), ("Private!", "Private!"), ("All super user", "All super user"), ("Protected", "Protected")])



class Calendarnofication(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateField()
    status = models.CharField(
        max_length=255, default="incompleted", blank=True, null=True
    )
  


class CustomFields(models.Model):
    field_belongs_to = models.CharField(max_length=500, choices=[("Student", "Student"), ("Staff", "Staff")])
    field_type = models.CharField(max_length=500, choices=[("input", "Input"), ("number", "Number"), ("textarea", "Textarea"), ("select", "Select"), ("multiselect", "Multi Select"), ("checkbox", "Checkbox"), ("Date", "Date Picker"), ("datetime-local", "Datetime Picker"), ("color", "Color Picker"), ("url", "HyperLink")])
    field_name = models.CharField(max_length=50)
    grid = models.IntegerField()
    field_value = models.TextField(blank=True, null=True)
    required = models.BooleanField()


class StudentCustomFieldValues(models.Model):
    field = models.ForeignKey(CustomFields, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)


class StaffCustomFieldValues(models.Model):
    field = models.ForeignKey(CustomFields, on_delete=models.CASCADE)
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE)
    value = models.TextField(blank=True, null=True)


class Modules(models.Model):
    system = models.TextField(blank=True, null=True)
    student = models.TextField(blank=True, null=True)
    parent = models.TextField(blank=True, null=True)


class Studentprofileupdate(models.Model):
    fieldshide = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, default="Enabled", blank=True, null=True)



class SystemFields(models.Model):
    student_fields = models.TextField(blank=True, null=True)
    staff_fields = models.TextField(blank=True, null=True)


class StudentDocuments(models.Model):
    student = models.ForeignKey(
        StudentAdmission, on_delete=models.CASCADE, blank=True, null=True
    )
    title = models.CharField(max_length=250)
    document = models.FileField(upload_to="Student Document/")
    session = models.ForeignKey(
        "sub_part.Session", on_delete=models.CASCADE, blank=True, null=True
    )



class StaffDocument(models.Model):
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to="Staffs Document/")
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE, blank=True, null=True)



class StaffTimeline(models.Model):
    staff = models.ForeignKey(AddStaff, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=250)
    date = models.DateField()
    description = models.TextField(max_length=500, blank=True, null=True)
    attact_document = models.FileField(blank=True, null=True)
    visible_to_this_person = models.BooleanField(default=True)


class PrintHeaderFooter(models.Model):
    image_fees_receipt = models.FileField(blank=True, null=True)
    image_payslip = models.FileField(blank=True, null=True)
    note_fees_receipt = models.TextField(blank=True, null=True)
    note_payslip = models.TextField(blank=True, null=True)
  
class OnlineClassAttendance(models.Model):
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE)
    online = models.ForeignKey(OnlineClass, on_delete=models.CASCADE)
    attendance_status = models.CharField(max_length=100)
    attendance_date = models.DateTimeField()
    status = models.CharField(max_length=100, blank=True, null=True)  

  
    


class DownloadRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(default=timezone.now)
    file_path = models.FilePathField(path='Backup',recursive=True)

    def __str__(self):
        return f"{self.user.username} downloaded {self.file_path} at {self.downloaded_at}"
    


class QuestionPaper(models.Model):
    question_paper_name = models.CharField(max_length=255)
    total_mark = models.IntegerField()
    pass_mark = models.IntegerField()
    duration = models.DurationField()
    


class Part(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE, related_name='parts')
    part_name = models.CharField(max_length=255)
    per_Question_mark = models.IntegerField()
    total_mark=models.IntegerField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.part_name} ({self.question_paper.question_paper_name})"

class Question(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    question_paper = models.ForeignKey(QuestionPaper, related_name='question_paper', on_delete=models.CASCADE)
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=[('choice', 'Multiple Choice'), ('paragraph', 'Paragraph')])
    options = models.JSONField(default=list,blank=True, null=True)  
    mark = models.IntegerField(blank=True, null=True)
    


    def save(self, *args, **kwargs):
        
        if self.part and self.mark is None:
            self.mark = self.part.per_Question_mark
        
        super().save(*args, **kwargs)

    def is_correct(self, selected_option):
        if self.question_type == 'choice' and self.options:
            return self.options.get(selected_option, {}).get('is_correct', False)
        return False

    def __str__(self):
        return f"Question in {self.part.part_name if self.part else 'No Part'} - {self.text[:50]}"


class Enrollment(models.Model):
    question_paper = models.ForeignKey(QuestionPaper, on_delete=models.CASCADE)    
    exam_date = models.DateField(blank=False, null=True)
    any_time = models.BooleanField(default=False)
    start_time = models.TimeField(blank=True, null=True)
    allowed_time = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=100, choices=[("assign", "Assign"), ("waiting", "Waiting"), ("completed", "Completed")])  
    
    
class EnrollmentAssign(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ManyToManyField(Section)  
       

   
class StudentAnswers(models.Model): 
    student = models.ForeignKey(
        "StudentAdmission", on_delete=models.CASCADE, null=True, blank=True
    )
    question_paper = models.ForeignKey(QuestionPaper, related_name='StudentAnswers_question_paper', on_delete=models.CASCADE)
          
    
class AnswerPeperSubmit(models.Model): 
    student_answers = models.ForeignKey(StudentAnswers, related_name='AnswerPeperSubmit_student_answers', on_delete=models.CASCADE)
    questiones = models.ForeignKey(Question, related_name='AnswerPeperSubmit_questions', on_delete=models.CASCADE)    
    options = models.JSONField(default=list,blank=True, null=True)  
    mark = models.IntegerField(blank=True, null=True)
    validation = models.BooleanField(default=False)
    

class PaperCorrection(models.Model): 
    student = models.ForeignKey(
        "StudentAdmission", on_delete=models.CASCADE, null=True, blank=True
    )
    question_paper = models.ForeignKey(QuestionPaper, related_name='PaperCorrection_question_paper', on_delete=models.CASCADE)
    total_mark =  models.IntegerField()
    is_pass = models.BooleanField(default=False)    
       
    
class Transaction(models.Model): 
    student = models.ForeignKey(StudentAdmission, on_delete=models.CASCADE, null=True, blank=True)
    reference_id =  models.CharField(max_length=800)
                


class Vendor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
  


    def __str__(self):
        return self.name
    
class Expense(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="expenses")
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE,
    related_name='expenses')    
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10000, decimal_places=2)   
    invoice_date = models.DateField()
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=[("Pending", "Pending"), ("Paid", "Paid"), ("generateinvoice", "Generate Invoice")], default="Pending")  
    payment_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    regular_payment = models.BooleanField(default=False)
    one_time_payment = models.BooleanField(default=False)
 
                

    def __str__(self):
        return f"{self.item_name} ({self.category.name})"
    
class Invoice(models.Model):
    expense = models.ManyToManyField(Expense, related_name='invoice',null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True, related_name="invoices")
    invoice_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status =  models.CharField(max_length=100,) 
    payment_date = models.DateField(null=True, blank=True)

                

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class StudentMain(models.Model):    
    admission_no = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=100,blank=True, null=True)  
    account = models.ForeignKey(
        "Account", on_delete=models.CASCADE, null=True, blank=True
    )
    first_name = models.CharField(max_length=500)
    last_name = models.CharField(max_length=500, blank=True, null=True)  
    gender = models.CharField(max_length=500, choices=[("Male", "Male"), ("Female", "Female")], blank=True, null=True)
    date_of_birth = models.DateField()
    category = models.ForeignKey(
        StudentCategory, on_delete=models.CASCADE, blank=True, null=True
    )  
    religion = models.CharField(max_length=500, blank=True, null=True)  
    Caste = models.CharField(max_length=500, blank=True, null=True)  
    mobile_number = models.CharField(max_length=500, blank=True, null=True)  
    email = models.EmailField(max_length=500, blank=True, null=True)  
    admission_date = models.DateField(default=date.today, blank=True, null=True)
    student_photo = models.FileField(blank=True, null=True)
    Blood_group = models.CharField(max_length=100, choices=[("O+", "O+"), ("A+", "A+"), ("B+", "B+"), ("AB+", "AB+"), ("O-", "O-"), ("A-", "A-"), ("B-", "B-"), ("AB-", "AB-")], blank=True, null=True)   
    height = models.CharField(max_length=500, blank=True, null=True)  
    weight = models.CharField(max_length=500, blank=True, null=True)  
    as_on_date = models.DateField(blank=True, null=True)  
    bank_account_number = models.CharField(max_length=500, blank=True, null=True)  
    bank_name = models.CharField(max_length=500, blank=True, null=True)  
    ifsc_code = models.CharField(max_length=500, blank=True, null=True)  
    national_identification_number = models.CharField(
        max_length=50, blank=True, null=True
    )
    local_identification_number = models.CharField(max_length=50, blank=True, null=True)
    rte = models.CharField(max_length=100, choices=[("Yes", "Yes"), ("No", "No")], default="No")
    previous_school_detail = models.TextField(max_length=250, blank=True, null=True)
    note = models.TextField(max_length=250, blank=True, null=True)

    title_1 = models.CharField(max_length=500, blank=True, null=True)
    documents_1 = models.FileField(blank=True, null=True)
    title_2 = models.CharField(max_length=500, blank=True, null=True)
    documents_2 = models.FileField(blank=True, null=True)
    title_3 = models.CharField(max_length=500, blank=True, null=True)
    documents_3 = models.FileField(blank=True, null=True)
    title_4 = models.CharField(max_length=500, blank=True, null=True)
    documents_4 = models.FileField(blank=True, null=True)
    disable_date = models.DateField(blank=True, null=True)
    diable_reson = models.ForeignKey(
        DisableReason, on_delete=models.CASCADE, blank=True, null=True
    )
    disable_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=250, default="Enable", blank=True, null=True)
    user_student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="StudentMain_user_student",
    )
    user_parent = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="StudentMain_user_parent",
    )
       
    student_health = models.CharField(max_length=100, blank=True, null=True)    
    student_health_description	= models.TextField(max_length=550, blank=True, null=True)
    name_of_last_school = models.CharField(max_length=250,blank=True, null=True)
    leaving_last_school_reason = models.TextField(max_length=550,blank=True, null=True)
    grade_completed = models.CharField(max_length=100, choices=[("Yes", "Yes"), ("No", "No")], blank=True, null=True)
    suspended_or_not = models.CharField(max_length=100, blank=True, null=True)
    is_suspension_resolved = models.CharField(max_length=100, blank=True, null=True) 
    suspension_reason = models.TextField(max_length=550,blank=True, null=True)
    county = models.CharField(max_length=250,blank=True, null=True)
    sub_county =  models.CharField(max_length=250,blank=True, null=True)
    ward = models.CharField(max_length=250,blank=True, null=True)
       
    source = models.CharField(max_length=250, default="offline",null=True, blank=True) 
    vehicle_number=models.ForeignKey('sub_part.vehicle',on_delete=models.CASCADE,blank=True,null=True)
    route_list=models.ForeignKey(Route,on_delete=models.CASCADE,blank=True,null=True)
    hostel=models.ForeignKey(Hostel,on_delete=models.CASCADE,blank=True,null=True)


    def get_or_generate_account_number(self):
        return f"SCH-{str(self.id)}"

    def get_school_account_number(self):
        return self.get_or_generate_account_number()

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.id}"
    

class StudentVaultAmount(models.Model): 
    student = models.ForeignKey(StudentMain, on_delete=models.CASCADE)
    total_amount = models.IntegerField(blank=True, null=True, default=0)
    paid_amount = models.IntegerField(blank=True, null=True, default=0)
    balance_amount = models.IntegerField(blank=True, null=True, default=0)
    session = models.ForeignKey("sub_part.Session", on_delete=models.CASCADE)

      
    
class AlumniType(models.Model):
    name = models.CharField(max_length=50, unique=True)  
    description = models.TextField(blank=True, null=True)  
      

    def __str__(self):
        return self.name 

class Alumni(models.Model):
    name = models.CharField(max_length=255)
    graduation_year = models.PositiveIntegerField()
    alumni_type = models.ForeignKey(AlumniType, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=15)
    current_location = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='alumni_pics/', null=True, blank=True)
    department = models.ForeignKey(Section,on_delete=models.CASCADE)
      


    def __str__(self):
        return self.name

class EventType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)  
      

    def __str__(self):
        return self.name

class AlumniEvents(models.Model):
    event_title = models.CharField(max_length=255) 
    event_date = models.DateField(null=True, blank=True)  
    location = models.CharField(max_length=255)  
    description = models.TextField()  
    event_time = models.TimeField(null=True, blank=True)  
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)  
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE,related_name="AlumniEvents_event_type")  
    event_status = models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('UPCOMING', 'Upcoming'), ('PAST', 'Past')], default='UPCOMING')
      

    def __str__(self):
        return self.event_title
    
class BuyerLoginCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buyer_username = models.CharField(max_length=50, blank=True, null=True)
    buyer_passwod = models.CharField(max_length=50, blank=True, null=True)
        
    
    
    

        