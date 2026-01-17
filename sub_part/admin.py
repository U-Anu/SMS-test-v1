from django.contrib import admin
from sub_part.models import *
from django.contrib import admin
from import_export import resources
from django.contrib.auth.admin import UserAdmin

from import_export.admin import ImportExportModelAdmin


# Register your models here.
admin.site.register(DownloadRecord)
admin.site.register(EmailSmsLog)

admin.site.register(OnlineExam)
# admin.site.register(AddStaff)
admin.site.register(Purpose)
admin.site.register(ComplainType)
admin.site.register(Source)
admin.site.register(Reference)

admin.site.register(StudentCategory)
admin.site.register(DisableReason)
admin.site.register(Route)
admin.site.register(Hostel)
admin.site.register(Incomehead)
admin.site.register(ExpenseHead)
admin.site.register(CaroselImage)
admin.site.register(Role)
admin.site.register(AddLeaveType)
admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(AddItem)
admin.site.register(ItemCategory)
admin.site.register(ItemStore)
admin.site.register(ItemSupplier)
admin.site.register(AdmissionEnquiry)
admin.site.register(VisitorBook)
admin.site.register(PhoneCallLog)
admin.site.register(PostalDispatch)
admin.site.register(PostalReceive)
admin.site.register(Complain)
admin.site.register(AddIncome)
admin.site.register(AddExpense)
admin.site.register(FeesTypeDiscount)
admin.site.register(Addleave)
admin.site.register(examGroup)
admin.site.register(AdmitCard)
admin.site.register(DesignMarkSheet)
admin.site.register(AddGrade)
admin.site.register(QuestionBank)
admin.site.register(Lesson)
admin.site.register(topic)
admin.site.register(AssignClassTeacher)
admin.site.register(Subjects)
admin.site.register(SubjectGroup)
admin.site.register(ApproveLeave)
admin.site.register(ApplyLeave)
admin.site.register(noticeBoard)
admin.site.register(UploadContent)
admin.site.register(AddHomeWork)
admin.site.register(AddBook)
admin.site.register(IssueBook)
admin.site.register(LibrayMember)
admin.site.register(IssueItem)
admin.site.register(ItemStock)
admin.site.register(Vehicle)
admin.site.register(AssignVehicle)
admin.site.register(HostelRoom)
admin.site.register(RoomType)
admin.site.register(StudentCertificate)
admin.site.register(StudentId)
admin.site.register(Event)
admin.site.register(MediaManager)
admin.site.register(Menu)
admin.site.register(AlumniEvent)
admin.site.register(Session)
admin.site.register(Managealumini)
admin.site.register(StudentAttendance)
admin.site.register(PayrollSummary)
# admin.site.register(User)
admin.site.register(AvailableLeave)
admin.site.register(TeacherRating)
admin.site.register(Infrastructure)
admin.site.register(SchoolHeads)
admin.site.register(FeesAssign)
admin.site.register(BasicWebPageDetails)
admin.site.register(Studentprofileupdate)
admin.site.register(PrintHeaderFooter)
admin.site.register(Modules)
admin.site.register(OnlineClass)
admin.site.register(StaffMeeting)
admin.site.register(ParentMeeting)
admin.site.register(LessonPlan  )
admin.site.register(TimeTable)
admin.site.register(GradingScale)
admin.site.register(GeneralSetting)
admin.site.register(DiscountAssign)


class SchoolYearAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ("year",)

admin.site.register(EducationLevel)
admin.site.register(SchoolYear, SchoolYearAdmin)
admin.site.register(AddExam)
admin.site.register(Term)
admin.site.register(AssetType)
admin.site.register(ChargeType)
admin.site.register(GLLine)
admin.site.register(TransactionCode)
admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(AccountEntry)
admin.site.register(TransactionType)
admin.site.register(PaymentRecord)
admin.site.register(GuardianMaster)
admin.site.register(StudentGuardianDetails)
admin.site.register(EmailSetting)
admin.site.register(StaffEducationQualification)
admin.site.register(OnlineClassAttendance)
admin.site.register(SchoolRegistration)
admin.site.register(StudentHouse)
admin.site.register(StudentCustomFieldValues)


admin.site.register(MeetingLinkMaster)
admin.site.register(StudentFess)
admin.site.register(Branch)
admin.site.register(GradingSystem)
admin.site.register(QuestionPaper)
admin.site.register(Question)
admin.site.register(Part)
admin.site.register(Enrollment)
admin.site.register(EnrollmentAssign)
admin.site.register(StudentAnswers)
admin.site.register(AnswerPeperSubmit)
admin.site.register(PaperCorrection)
admin.site.register(Currency)
admin.site.register(Transaction)
admin.site.register(PromoteStudent)
admin.site.register(ExamStudent)
admin.site.register(StaffLeave)
admin.site.register(AddExamSubject)
admin.site.register(ExpenseCategory)
admin.site.register(Expense)
admin.site.register(Invoice)
admin.site.register(EntryMarks)
admin.site.register(Vendor)
admin.site.register(Notification)
admin.site.register(Feedback)
admin.site.register(Feedback_Reasons)


admin.site.register(AlumniType)
admin.site.register(Alumni)
admin.site.register(EventType)
admin.site.register(AlumniEvents)
admin.site.register(ItemStockDeatail)
admin.site.register(SystemFields)
admin.site.register(ExamType)

# Register your models here.
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'first_name']
admin.site.register(User, UserAdmin)

# Register your models here.
class StudentAdmissionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'admission_no','first_name']
admin.site.register(StudentAdmission, StudentAdmissionAdmin)



class StudentMainAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'first_name']
admin.site.register(StudentMain, StudentMainAdmin)


class LoginCredentialsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'student_username']
admin.site.register(LoginCredentials, LoginCredentialsAdmin)

class StudentSessionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'student']
admin.site.register(StudentSession, StudentSessionAdmin)



class StudentClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'student']
admin.site.register(StudentClass, StudentClassAdmin)


class StudentVaultAmountAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'total_amount']
admin.site.register(StudentVaultAmount, StudentVaultAmountAdmin)


class AddStaffAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'staff_id']
admin.site.register(AddStaff, AddStaffAdmin)



class ClassAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'Class']
admin.site.register(Class, ClassAdmin)


class SectionAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'section_name']
admin.site.register(Section, SectionAdmin)


class FeesGroupAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'name']
admin.site.register(FeesGroup, FeesGroupAdmin)


class FeesTypeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'name']
admin.site.register(FeesType, FeesTypeAdmin)


class FeesMasterAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    '''
    this is for if we have default primary key like id
    '''
    list_display = ['id', 'amount']
admin.site.register(FeesMaster, FeesMasterAdmin)


admin.site.register(Company1)
admin.site.register(Employee)
admin.site.register(UserSubscription)
 