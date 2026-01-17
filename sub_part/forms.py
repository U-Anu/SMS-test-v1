from django import forms
from sub_part.models import *



class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "middle_name",
            "last_name",
            "email",
            "phone_number",
            "dob",
            "username",
            "password",
            "buyer_id"
        ]
        widgets = {
            "dob": forms.DateInput(attrs={"type": "date"}),
        }
        labels={
           "buyer_id":"Customer id"
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not username.endswith("@gmail.com"):
            raise forms.ValidationError("Username must end with '@gmail.com'.")
        return username
            
           


class PurposeForm(forms.ModelForm):
    class Meta:
        model = Purpose
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(PurposeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ComplainTypeForm(forms.ModelForm):
    class Meta:
        model = ComplainType
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ComplainTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(SourceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ReferenceForm(forms.ModelForm):
    class Meta:
        model = Reference
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ReferenceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AdmissionEnquiryForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "dob": forms.DateInput(attrs={"type": "date"}),
            "next_follow_up_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels={
            "branch":"",
            "reference":"Refer By"
        }

    def __init__(self, *args, **kwargs):
        super(AdmissionEnquiryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class VisitorBookForm(forms.ModelForm):
    class Meta:
        model = VisitorBook
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),    
            "out_time": forms.TimeInput(attrs={"type": "time"}),
            "in_time": forms.TimeInput(attrs={"type": "time"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(VisitorBookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class PhoneCallLogForm(forms.ModelForm):
    class Meta:
        model = PhoneCallLog
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
            "next_follow_up_date": forms.DateInput(attrs={"type": "date"}),
            "call_type": forms.RadioSelect(),
        }
        labels = {
            "branch": "",
        }


    def __init__(self, *args, **kwargs):
        super(PhoneCallLogForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class PostalDispatchForm(forms.ModelForm):
    class Meta:
        model = PostalDispatch
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(PostalDispatchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class PostalReceiveForm(forms.ModelForm):
    class Meta:
        model = PostalReceive
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(PostalReceiveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ComplainForm(forms.ModelForm):
    class Meta:
        model = Complain
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(ComplainForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentAdmissionForm(forms.ModelForm):
    class Meta:
        model = StudentAdmission
        exclude = ("session","student_main","user_student","user_parent")
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "admission_date": forms.DateInput(attrs={"type": "date"}),
            "as_on_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop("branch", None)  # 👈 get branch
        super().__init__(*args, **kwargs)

        # Add Bootstrap class
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        # Branch-wise filtering
        if branch:
            if "Class" in self.fields:
                self.fields["Class"].queryset = Class.objects.filter(branch=branch)

            if "section" in self.fields:
                self.fields["section"].queryset = Section.objects.filter(branch=branch)
            
            if "category" in self.fields:
                self.fields["category"].queryset = StudentCategory.objects.filter(branch=branch)
            if "route_list" in self.fields:
                self.fields["route_list"].queryset = Route.objects.filter(branch=branch)
            if "hostel" in self.fields:
                self.fields["hostel"].queryset = Hostel.objects.filter(branch=branch)
            if "vehicle_number" in self.fields:
                self.fields["vehicle_number"].queryset = Vehicle.objects.filter(branch=branch)
        # Make admission_no field read-only
        # if "admission_no" in self.fields:
        #     self.fields["admission_no"].widget.attrs["readonly"] = True

class StudentCategoryForm(forms.ModelForm):
    class Meta:
        model = StudentCategory
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(StudentCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentHouseForm(forms.ModelForm):
    class Meta:
        model = StudentHouse
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StudentHouseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class DisableReasonForm(forms.ModelForm):
    class Meta:
        model = DisableReason
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(DisableReasonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = AddIncome
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(AddIncomeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AssetTypeForm(forms.ModelForm):
    class Meta:
        model = AssetType
        fields = "__all__"
       
        widgets = {
            "branch": forms.HiddenInput(),
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "branch": "",
        }

    def __init__(self, *args, **kwargs):
        super(AssetTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ChargeTypeForm(forms.ModelForm):
    class Meta:
        model = ChargeType
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(ChargeTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class GLLineForm(forms.ModelForm):
    class Meta:
        model = GLLine
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(GLLineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AccountTypeForm(forms.ModelForm):
    class Meta:
        model = AccountType
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),       
            "branch": forms.HiddenInput(),     
        }   
      
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AccountTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# class ChargeTypeForm(forms.ModelForm):
#     class Meta:
#         model = ChargeType
#         fields = "__all__"
#         widgets = {
#             "date": forms.DateInput(attrs={"type": "date"}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(ChargeTypeForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),        
            "branch": forms.HiddenInput(),        
            "due_date": forms.DateInput(attrs={"type": "date"}),   
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AccountEntryForm(forms.ModelForm):
    class Meta:
        model = AccountEntry
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class TransactionCodeForm(forms.ModelForm):
    class Meta:
        model = TransactionCode
        fields = "__all__"


class TransactionTypeForm(forms.ModelForm):
    class Meta:
        model = TransactionType
        fields = "__all__"


class FeesMasterForm(forms.ModelForm):
    class Meta:
        model = FeesMaster
        exclude = ("status",)
   
        widgets = {
            "branch": forms.HiddenInput(),        
            "due_date": forms.DateInput(attrs={"type": "date"}),   
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(FeesMasterForm, self).__init__(*args, **kwargs)
        self.fields["fees_group"].queryset = FeesGroup.objects.exclude(
            name="Balance Master"
        )
        self.fields["fees_type"].queryset = FeesType.objects.exclude(
            name="Previous Session Balance", Fees_code="Previous Session Balance"
        )
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FeesGroupForm(forms.ModelForm):
    class Meta:
        model = FeesGroup
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),        
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(FeesGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FeesTypeDiscountForm(forms.ModelForm):
    class Meta:
        model = FeesTypeDiscount
        exclude = ("percentage_amount",)
        widgets = {
            "branch": forms.HiddenInput(),        
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(FeesTypeDiscountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class IncomeheadForm(forms.ModelForm):
    class Meta:
        model = Incomehead
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),        
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(IncomeheadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class FeesTypeForm(forms.ModelForm):
    class Meta:
        model = FeesType
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),        
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(FeesTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# Expense
class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = AddExpense
        fields = "__all__"
    
        widgets = {
            "branch": forms.HiddenInput(),   
            "date": forms.DateInput(attrs={"type": "date"}),
     
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddExpenseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ExpenseHeadForm(forms.ModelForm):
    class Meta:
        model = ExpenseHead
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),   
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseHeadForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddleaveForm(forms.ModelForm):
    class Meta:
        model = Addleave
        exclude = ("status", "created_by", "session", "approved_by")
        widgets = {
            "apply_date": forms.DateInput(attrs={"type": "date"}),
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
            "branch": forms.HiddenInput(),   
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddleaveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddleaveParentForm(forms.ModelForm):
    class Meta:
        model = Addleave
        fields = "__all__"
        widgets = {
            "Class": forms.HiddenInput(),
            "section": forms.HiddenInput(),
            "student": forms.HiddenInput(),
            "apply_date": forms.DateInput(attrs={"type": "date"}),
            "from_date": forms.DateInput(attrs={"type": "date"}),
            "to_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.HiddenInput(),
            "branch": forms.HiddenInput(),   

        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddleaveParentForm, self).__init__(*args, **kwargs)
        # Set initial value for status field once
        self.fields['status'].initial = "Pending"
        
        # Apply 'form-control' class to all visible fields
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class examGroupForm(forms.ModelForm):
    class Meta:
        model = examGroup
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),   
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(examGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AdmitCardForm(forms.ModelForm):
    class Meta:
        model = AdmitCard
        fields = "__all__"
        widgets = {
            "name": forms.CheckboxInput(),
            "father_name": forms.CheckboxInput(),
            "mother_name": forms.CheckboxInput(),
            "date_of_birth": forms.CheckboxInput(),
            "admission_no": forms.CheckboxInput(),
            "roll_no": forms.CheckboxInput(),
            "address": forms.CheckboxInput(),
            "gender": forms.CheckboxInput(),
            "photo": forms.CheckboxInput(),
            "Class": forms.CheckboxInput(),
            "section": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(AdmitCardForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class DesignMarkSheetForm(forms.ModelForm):
    class Meta:
        model = DesignMarkSheet
        fields = "__all__"
        widgets = {
            "printing_date": forms.DateInput(attrs={"type": "date"}),
            "name": forms.CheckboxInput(),
            "father_name": forms.CheckboxInput(),
            "mother_name": forms.CheckboxInput(),
            "date_of_birth": forms.CheckboxInput(),
            "admission_no": forms.CheckboxInput(),
            "roll_no": forms.CheckboxInput(),
            "address": forms.CheckboxInput(),
            "gender": forms.CheckboxInput(),
            "photo": forms.CheckboxInput(),
            "grade": forms.CheckboxInput(),
            "section": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(DesignMarkSheetForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddGradeForm(forms.ModelForm):
    class Meta:
        model = AddGrade
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddGradeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AssignSubjectForm(forms.ModelForm):
    class Meta:
        model = AssignSubject
        fields = "__all__"
        widgets = {
            "subject": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AssignSubjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class OnlineExamForm(forms.ModelForm):
    class Meta:
        model = OnlineExam
        fields = "__all__"
        widgets = {
            "exam_from": forms.DateInput(attrs={"type": "date"}),
            "exam_to": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(OnlineExamForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class QuestionBankForm(forms.ModelForm):
    class Meta:
        model = QuestionBank
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(QuestionBankForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class topicForm(forms.ModelForm):
    class Meta:
        model = topic
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(topicForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AssignClassTeacherForm(forms.ModelForm):
    class Meta:
        model = AssignClassTeacher
        exclude = ("session",)
        widgets = {
            "class_teacher": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AssignClassTeacherForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AssignSubjectTeacherForm(forms.ModelForm):
    class Meta:
        model = AssignSubjectTeacher
        exclude = ("session",)
        widgets = {
            "subject": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AssignSubjectTeacherForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SubjectsForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(SubjectsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SubjectGroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = "__all__"
        widgets = {
            "subject": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SubjectGroupForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(), 
            "section_name": forms.TextInput(attrs={"type": "text", "class": "form-control"}), 
        }
        labels = {
            "branch": "",  # Empty label for "branch"
            "section_name": "Stream  Name",  # Correct label for "name"
        }

    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = "__all__" 
        widgets = {
            "section": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ClassRegisterForm(forms.ModelForm):
    class Meta:
        model = ClassRegister
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ClassRegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

            # changes


class SchoolCompositionForm(forms.ModelForm):
    class Meta:
        model = SchoolCompositions
        fields = ["description", "no_of_years", "Class"]
        widgets = {
            "Class": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolCompositionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# level of education
class EducationLevelForm(forms.ModelForm):
    class Meta:
        model = EducationLevel
        fields = ["level", "description", "composition"]
        widgets = {
            "composition": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(EducationLevelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# grading system
class GradingSystemForm(forms.ModelForm):
    class Meta:
        model = GradingSystem
        fields = ["name", "Class", "scale", "points", "pass_remarks", "fail_remarks"]

    def clean_scale(self):
        scale = self.cleaned_data.get("scale")
        if scale < 1:
            raise forms.ValidationError("Scale must be a positive integer.")
        return scale

    def clean_points(self):
        points = self.cleaned_data.get("points")
        if points < 1:
            raise forms.ValidationError("Points must be a positive integer.")
        return points

    def __init__(self, *args, **kwargs):
        super(GradingSystemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ApproveLeaveForm(forms.ModelForm):
    class Meta:
        model = ApproveLeave
        exclude = (
            "number_of_days",
            "created_by",
        )
        widgets = {
            "apply_date": forms.DateInput(attrs={"type": "date"}),
            "leave_date_from": forms.DateInput(attrs={"type": "date"}),
            "leave_date_to": forms.DateInput(attrs={"type": "date"}),
            "status": forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(ApproveLeaveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ApplyLeaveForm(forms.ModelForm):
    class Meta:
        model = ApplyLeave
        fields = "__all__"
        widgets = {
            "leave_date_from": forms.DateInput(attrs={"type": "date"}),
            "leave_date_to": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(ApplyLeaveForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddLeaveTypeForm(forms.ModelForm):
    class Meta:
        model = AddLeaveType
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddLeaveTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CurriculumForm(forms.ModelForm):
    class Meta:
        model = Curriculum
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CurriculumForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        # school


# class SchoolForm(forms.ModelForm):
#     class Meta:
#         model = School
#         fields = [
#             "name",
#             "country",
#             "company",
#             "head_teacher",
#             "admin_in_charge",
#             "hr_in_charge",
#         ]
#         # Add widgets/customize form fields if needed

#     def __init__(self, *args, **kwargs):
#         super(SchoolForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs["class"] = "form-control"

    # school year


class SchoolYearForm(forms.ModelForm):
    class Meta:
        model = SchoolYear
        fields = [
            "year",
            "term",
        ]
        widgets = {
            "term": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolYearForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    # term


class TermForm(forms.ModelForm):
    class Meta:
        model = Term
        fields = [
            "term_name",
            "start_date",
            "end_date",
        ]
        widgets = {
            "start_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(TermForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class DesignationForm(forms.ModelForm):
    class Meta:
        model = Designation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(DesignationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class noticeBoardForm(forms.ModelForm):
    class Meta:
        model = noticeBoard
        fields = "__all__"
        widgets = {
            "notice_date": forms.DateInput(attrs={"type": "date"}),
            "publish_on": forms.DateInput(attrs={"type": "date"}),
            "message_to": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(noticeBoardForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class UploadContentForm(forms.ModelForm):
    class Meta:
        model = UploadContent
        fields = "__all__"
        widgets = {
            "upload_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(UploadContentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddHomeWorkForm(forms.ModelForm):
    class Meta:
        model = AddHomeWork
        fields = "__all__"
        widgets = {
            "homework_date": forms.DateInput(attrs={"type": "date"}),
            "submission_date": forms.DateInput(attrs={"type": "date"}),
            "evaluation_date": forms.DateInput(attrs={"type": "date"}),
            "branch": forms.HiddenInput(),
        }
        labels={
            "branch":""
        }
        

    def __init__(self, *args, **kwargs):
        super(AddHomeWorkForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddBookForm(forms.ModelForm):
    class Meta:
        model = AddBook
        exclude = ("available_qty",)
        widgets = {
            "post_date": forms.DateInput(attrs={"type": "date"}),
            "branch": forms.HiddenInput(),
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# Inventory


class IssueItemForm(forms.ModelForm):
    class Meta:
        model = IssueItem
        exclude = ("status",)

    def __init__(self, *args, **kwargs):
        super(IssueItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# -----Non returnable item----------------------------
class NonReturnableItemForm(forms.ModelForm):
    class Meta:
        model = NonReturnableItem
        fields = "__all__"


class ItemStockForm(forms.ModelForm):
    class Meta:
        model = ItemStock
        fields = [
            "item_category",
            "item",
            "supplier",
            "store",
            "quantity",
            "purchase_price",
            "date",
            "attach_document",
            "description",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(ItemStockForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ItemStockDeatailForm(forms.ModelForm):
    class Meta:
        model = ItemStockDeatail
        fields = "__all__"


class AddItemForm(forms.ModelForm):
    class Meta:
        model = AddItem
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddItemForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ItemCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ItemCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ItemStoreForm(forms.ModelForm):
    class Meta:
        model = ItemStore
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ItemStoreForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ItemSupplierForm(forms.ModelForm):
    class Meta:
        model = ItemSupplier
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ItemSupplierForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(RouteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(VehicleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AssignVehicleForm(forms.ModelForm):
    class Meta:
        model = AssignVehicle
        fields = "__all__"
        widgets = {
            "vehicle": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AssignVehicleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class HostelRoomForm(forms.ModelForm):
    class Meta:
        model = HostelRoom
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(HostelRoomForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(RoomTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class HostelForm(forms.ModelForm):
    class Meta:
        model = Hostel
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(HostelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentCertificateForm(forms.ModelForm):
    background_image = forms.FileField(label="Background image", required=True)

    class Meta:
        model = StudentCertificate
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StudentCertificateForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentIdForm(forms.ModelForm):
    class Meta:
        model = StudentId
        fields = "__all__"
        widgets = {
            "admission_no": forms.CheckboxInput(),
            "student_name": forms.CheckboxInput(),
            "Class": forms.CheckboxInput(),
            "father_name": forms.CheckboxInput(),
            "mother_name": forms.CheckboxInput(),
            "student_address": forms.CheckboxInput(),
            "date_of_birth": forms.CheckboxInput(),
            "phone": forms.CheckboxInput(),
            "blood_group": forms.CheckboxInput(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentIdForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "event_start": forms.DateInput(attrs={"type": "date"}),
            "event_end": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class MediaManagerForm(forms.ModelForm):
    class Meta:
        model = MediaManager
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MediaManagerForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class MenuForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MenuForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AlumniEventForm(forms.ModelForm):
    sms = forms.BooleanField(label="Send SMS", required=False)
    email = forms.BooleanField(label="Send Email", required=False)

    class Meta:
        model = AlumniEvent
        fields = "__all__"
        widgets = {
            "event_date_from": forms.DateInput(attrs={"type": "date"}),
            "event_date_to": forms.DateInput(attrs={"type": "date"}),
            "section": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(AlumniEventForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = "__all__"
        widgets = {
            "Section": forms.CheckboxSelectMultiple(),      
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = "__all__"
        widgets = {
            "Section": forms.CheckboxSelectMultiple(),      
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(RoleForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddStaffForm(forms.ModelForm):
    class Meta:
        model = AddStaff
        fields = "__all__"
        exclude = ("school",)
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "date_of_joining": forms.DateInput(attrs={"type": "date"}),
            "user": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
        }
        

    def __init__(self, *args, **kwargs):
        super(AddStaffForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class TimelineForm(forms.ModelForm):
    class Meta:
        model = Timeline
        fields = [
            "title",
            "date",
            "description",
            "attact_document",
            "visible_to_this_person",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(TimelineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentDocumentsForm(forms.ModelForm):
    class Meta:
        model = StudentDocuments
        fields = ["title", "document"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(StudentDocumentsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddExamForm(forms.ModelForm):
    class Meta:
        model = AddExam
        exclude = ("exam_group",)
        widgets = {
            "branch": forms.HiddenInput(),
        }
        lables ={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddExamForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class AddExamSubjectForm(forms.ModelForm):
    class Meta:
        model = AddExamSubject
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
        }
        lables ={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(AddExamSubjectForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

class ExamTypeForm(forms.ModelForm):
    class Meta:
        model = ExamType
        fields = ["name", "description"]
        widgets = {
            "branch": forms.HiddenInput(),
        }
        lables ={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(ExamTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

class ManagealuminiForm(forms.ModelForm):
    class Meta:
        model = Managealumini
        fields = "__all__"
        widgets = {
            "students_id": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super(ManagealuminiForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# class YesModelForm(forms.ModelForm):
#     class Meta:
#         model=YesModel
#         fields = ['yes_or_no']
#         widgets = {
#             'yes_or_no': forms.RadioSelect(choices=[(True, 'Yes'), (False, 'No')], attrs={'class': 'radio-inline'})
#         }
class GeneralSettingForm(forms.ModelForm):
    class Meta:
        model = GeneralSetting
        fields = "__all__"
        widgets = {
            "dateFormat": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        branch = kwargs.pop("branch", None)  # 👈 get branch
        super().__init__(*args, **kwargs)
        super(GeneralSettingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

        if branch:
            if "session" in self.fields:
                self.fields["session"].queryset = Session.objects.filter(branch=branch)

class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(StudentAttendanceForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class BasicWebPageDetailsForm(forms.ModelForm):
    class Meta:
        model = BasicWebPageDetails
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(BasicWebPageDetailsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


# class CaroselImageForm(forms.ModelForm):
#     carosel_image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': False}))
#     class Meta:
#         model = CaroselImage
#         fields = ['carosel_image']

#     def __init__(self, *args, **kwargs):
#         super(CaroselImageForm, self).__init__(*args, **kwargs)
#         for visible in self.visible_fields():
#             visible.field.widget.attrs['class'] = 'form-control'
class CaroselImageForm(forms.ModelForm):
    class Meta:
        model = CaroselImage
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CaroselImageForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(InfrastructureForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class EventsForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = "__all__"
        widgets = {
            "event_start_date": forms.DateInput(attrs={"type": "date"}),
            "event_end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(EventsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SchoolStaffForm(forms.ModelForm):
    class Meta:
        model = SchoolStaff
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SchoolStaffForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SchoolHeadsForm(forms.ModelForm):
    class Meta:
        model = SchoolHeads
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SchoolHeadsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class OffersForm(forms.ModelForm):
    class Meta:
        model = Offers
        fields = "__all__"
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(OffersForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class WebEnquiryForm(forms.ModelForm):
    class Meta:
        model = WebEnquiry
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(WebEnquiryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class SendEmailForm(forms.ModelForm):
    class Meta:
        model = SendEmail
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(SendEmailForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class OnlineClassForm(forms.ModelForm):
    class Meta:
        model = OnlineClass
        exclude = ("created_by","meeting_link")
        widgets = {
            "section": forms.CheckboxSelectMultiple(),
            "class_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super(OnlineClassForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"



class StaffMeetingForm(forms.ModelForm):
    class Meta:
        model = StaffMeeting
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "staff": forms.CheckboxSelectMultiple(),
            "start_time": forms.DateTimeInput(attrs={"type": "time"}),
            "end_time": forms.DateTimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffMeetingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ParentMeetingForm(forms.ModelForm):
    class Meta:
        model = ParentMeeting
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "staff": forms.CheckboxSelectMultiple(),
            "start_time": forms.DateTimeInput(attrs={"type": "time"}),
            "end_time": forms.DateTimeInput(attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super(ParentMeetingForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentmeetingnoteForm(forms.ModelForm):
    class Meta:
        model = Studentmeetingnote
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "staff": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentmeetingnoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StaffMeetingNoteForm(forms.ModelForm):
    class Meta:
        model = StaffMeetingNote
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "staff": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(StaffMeetingNoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class ParentMeetingNoteForm(forms.ModelForm):
    class Meta:
        model = ParentMeetingNote
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "staff": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ParentMeetingNoteForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class EventCalendarForm(forms.ModelForm):
    class Meta:
        model = EventCalendar
        exclude = ("created_by",)
        widgets = {
            "meeting_date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super(EventCalendarForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CalendarnoficationForm(forms.ModelForm):
    class Meta:
        model = Calendarnofication
        exclude = (
            "created_by",
            "status",
        )
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(CalendarnoficationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class CustomFieldsForm(forms.ModelForm):
    class Meta:
        model = CustomFields
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CustomFieldsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StudentsHideFieldForm(forms.ModelForm):
    class Meta:
        model = StudentAdmission
        fields = "__all__"
        widgets = {
            "user": forms.HiddenInput(),
            "created_by": forms.HiddenInput(),
            "roll_number": forms.HiddenInput(),
            "Class": forms.HiddenInput(),
            "section": forms.HiddenInput(),
            "if_permanent_address_is_current_address": forms.HiddenInput(),
            "room_number": forms.HiddenInput(),
            "note": forms.HiddenInput(),
            "title_1": forms.HiddenInput(),
            "documents_1": forms.HiddenInput(),
            "title_2": forms.HiddenInput(),
            "documents_2": forms.HiddenInput(),
            "documents_3": forms.HiddenInput(),
            "title_4": forms.HiddenInput(),
            "documents_4": forms.HiddenInput(),
            "disable_date": forms.HiddenInput(),
            "diable_reson": forms.HiddenInput(),
            "disable_note": forms.HiddenInput(),
            "status": forms.HiddenInput(),
            "user_student": forms.HiddenInput(),
            "user_parent": forms.HiddenInput(),
            "admission_no": forms.HiddenInput(),
            "as_on_date": forms.HiddenInput(),
            "student_health": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(StudentsHideFieldForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StaffDocumentForm(forms.ModelForm):
    class Meta:
        model = StaffDocument
        fields = ["title", "document"]

    def __init__(self, *args, **kwargs):
        super(StaffDocumentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"


class StaffTimelineForm(forms.ModelForm):
    class Meta:
        model = StaffTimeline
        fields = [
            "title",
            "date",
            "description",
            "attact_document",
            "visible_to_this_person",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffTimelineForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            
class GuardianMasterForm(forms.ModelForm):
    class Meta:
        model = GuardianMaster
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }


    def __init__(self, *args, **kwargs):
        super(GuardianMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"   

class MeetingLinkMasterForm(forms.ModelForm):
    class Meta:
        model = MeetingLinkMaster
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),           
        }
        labels={
            "branch":""
        }

    def __init__(self, *args, **kwargs):
        super(MeetingLinkMasterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"      

class SchoolRegistrationForm(forms.ModelForm):
    class Meta:
        model = SchoolRegistration
        widgets = {
            "end_of_financial_year": forms.DateInput(attrs={"type": "date"}),
            "end_of_month_date": forms.DateInput(attrs={"type": "date"}),
        }
        exclude = (
            "created_at",
            "branch",
            "school_id",
            "reference_id"
        )
    
    def __init__(self, *args, **kwargs):
        super(SchoolRegistrationForm, self).__init__(*args, **kwargs)
        # Apply Bootstrap class to each visible field
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        
        # Make specific fields required
        required_fields = [
           
            "address",
            "last_name",
            "phone_number",
            "email",
            "incorporation_number",
            "website",
            "number_of_branches",
            "number_of_staffs",
            "end_of_financial_year",
            "end_of_month_date",
            "amount_rounded_to",
            "local_currency"
        ]
        
        for field in required_fields:
            if field in self.fields:
                self.fields[field].required = True                     
            
            
#================20/08=================


class QuestionPaperForm(forms.ModelForm):
    class Meta:
        model = QuestionPaper
        fields = "__all__"
    def __init__(self, *args, **kwargs):
        super(QuestionPaperForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control" 


class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"   

class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        exclude = ("reference_id",)
        widgets = {
            "branch": forms.HiddenInput(),
            "reference_id": forms.HiddenInput(),
        }
        labels = {
            "branch": "",
            "reference_id": "",
        }
    
    def __init__(self, *args, **kwargs):
        super(CurrencyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
        
        # Set required fields
        self.fields['currency_code'].required = True
        self.fields['currency_name'].required = True
        self.fields['symbol'].required = True

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"      


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "question_paper": forms.HiddenInput(),
            "Class": forms.HiddenInput(),
            "section": forms.HiddenInput(),
            "exam_date": forms.DateInput(attrs={"type": "date"}),            
            "start_time": forms.TimeInput(attrs={"type": "time"})                       
        }
        labels={
            "branch":"",
            "question_paper":"",
            "Class":"",
            "section":""           
            
        }        

    def __init__(self, *args, **kwargs):
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
            
class EnrollmentAssignForm(forms.ModelForm):
    class Meta:
        model = EnrollmentAssign
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super(PartForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"     
            
  
            
class ExpenseCategoryForm(forms.ModelForm):
    class Meta:
        model = ExpenseCategory
        exclude = ("created_by",) 
        widgets = {
            "branch": forms.HiddenInput(),  
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseCategoryForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"    
            
class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        exclude = ("created_by",) 
        widgets = {
            "branch": forms.HiddenInput(),  
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"                
            
  
            
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ("created_by","status","regular_payment","one_time_payment")
        widgets = {
            "invoice_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "due_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "payment_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "branch": forms.HiddenInput(),
            
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"   
            
class AluminitypeForm(forms.ModelForm):
    class Meta:
        model = AlumniType
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(AluminitypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

# ==============================Start Alumni===========================
class AlumniForm(forms.ModelForm):
    class Meta:
        model = Alumni
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(AlumniForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

class EventTypeForm(forms.ModelForm):
    class Meta:
        model = EventType
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(EventTypeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

class AlumniEventsForm(forms.ModelForm):
    class Meta:
        model = AlumniEvents
        fields = "__all__"
        widgets = {
            "branch": forms.HiddenInput(),
            "event_date": forms.DateInput(attrs={"type": "date"}),
            "event_time": forms.TimeInput(attrs={"type": "time"}),
        }
        labels = {
            "branch": ""
        }

    def __init__(self, *args, **kwargs):
        super(AlumniEventsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"      
            
# ==============================End Alumni=============================                                                      