from rest_framework import serializers
from sub_part.models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
#Serializers of models

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Include user_type in the token payload
        token['user_type'] = user.user_type  # Replace 'user_type' with your actual user type field

        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_type'] = self.user.user_type  # Replace 'user_type' with your actual user type field
        return data


class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentAdmission
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','first_name','middle_name','last_name','password','phone_number',]
        extra_kwargs ={
            'password': {'write_only': True}
        }

    def create(self,validated_data):
        password= validated_data.pop('password',None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentAdmission
        fields='__all__'

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model=Class
        fields=['Class']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=['section_name']

class SubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubjectGroup
        fields=['name']

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Subjects
        fields=['subject_name','subject_type','subject_code']

class ViewHomeWorkSerializer(serializers.ModelSerializer):
    # created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    Class=ClassSerializer()
    section=SectionSerializer()
    subject_group=SubjectGroupSerializer()
    subject=SubjectsSerializer()
    class Meta:
        model = AddHomeWork
        exclude=('evaluation_date',)

class AddHomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddHomeWork
        exclude=('evaluation_date',)


class AssingHomeWorkSerializer(serializers.ModelSerializer):
    home_work=AddHomeWorkSerializer()
    class Meta:
        model=AssingHomeWork
        fields='__all__'

class HomeWorkSerializer(serializers.Serializer):
    homework_id = serializers.IntegerField(required=True)
    message = serializers.CharField(required=True)
    attach_document = serializers.FileField(allow_null=True, required=True)

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentAttendance
        fields='__all__'


# class AddHomeWorkSerializer(serializers.ModelSerializer):
#     # created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
#     Class=ClassSerializer()
#     section=SectionSerializer()
#     subject_group=SubjectGroupSerializer()
#     subject=SubjectsSerializer()
#     class Meta:
#         model = AddHomeWork
#         exclude=('evaluation_date',)

class SectionIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class ClassIDSerializer(serializers.ModelSerializer):
    # sections = SectionSerializer(many=True, read_only=True)

    class Meta:
        model = Class
        fields = ['id','Class']

class SubjectGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectGroup
        fields = ['id','name']

class SubjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

class SubjectIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','middle_name','last_name']

class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = ['id','first_name','last_name']


class ViewleaveSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    created_by=UserSerializer()
    approved_by=UserSerializer()
    student=StudentAdmissionSerializer()
    class Meta:
        model = Addleave
        # exculde = ['status','created_by','session','approved_by']
        exclude = ('session',)

class AddleaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=Addleave
        fields='__all__'
        exclude=('status','approved_by')


class AddLeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddLeaveType
        fields = ['id','name']

class StaffLeaveSerializer(serializers.ModelSerializer):
    leave_type=AddLeaveTypeSerializer()
    class Meta:
        model = StaffLeave
        fields = ['leave_type']

class AvailableLeaveSerializer(serializers.ModelSerializer):
    staff_leave=StaffLeaveSerializer()
    class Meta:
        model = AvailableLeave
        fields = ['available_leave','staff_leave']

class StaffLeaveViewSerializer(serializers.ModelSerializer):
    leave_type=AddLeaveTypeSerializer()
    class Meta:
        model=ApproveLeave
        exclude=('status','created_by','role','name')

class StaffLeaveAddSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApproveLeave
        exclude=('status','created_by','created_at','role','name','note')

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields = '__all__'

class AssignVehiclSerializer(serializers.ModelSerializer):
    class Meta:
        model=AssignVehicle
        fields = '__all__'

class RountSerializer(serializers.ModelSerializer):
    class Meta:
        model=Route
        fields = '__all__'


class RountSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Route
        fields = ['route_title']

class VehicleSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields = ['vehicle_number']

class StaffAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model=StaffAttendance
        fields = '__all__'

class StaffRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Role
        fields = ['name']

class AddleaveSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    created_by=UserSerializer()
    approved_by=UserSerializer()
    student=StudentAdmissionSerializer()
    class Meta:
        model = Addleave
        exclude = ('session',)

class HostelSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hostel
        fields = '__all__'

class RoomTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=RoomType
        fields = '__all__'

class HostelRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=HostelRoom
        fields = '__all__'

class StudentHostelSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentAdmission
        fields='__all__'

class StudentAdmissionHostelSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = ['hostel']

class StudentAttendanceSerializer1(serializers.ModelSerializer):
    class Meta:
        model=StudentAttendance
        fields = ['user_student']

class StaffAttendanSerializer1(serializers.ModelSerializer):
    class Meta:
        model=AddStaff
        fields = ['user']

class HostelSerializer1(serializers.ModelSerializer):
    class Meta:
        model=Hostel
        fields = ['hostel_type']

class RoomTypeSerializer1(serializers.ModelSerializer):
    class Meta:
        model=RoomType
        fields = ['room_type']

class SubjectsnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['subject_name']

class LessonSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    subject_group=SubjectGroupSerializer()
    subject=SubjectsnameSerializer()
    class Meta:
        model=Lesson
        fields = '__all__'

class LessonnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['lesson_name']

class topicSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    subject_group=SubjectGroupSerializer()
    subject=SubjectsnameSerializer()
    lesson_name=LessonnameSerializer()
    class Meta:
        model=topic
        fields = '__all__'

class topicnameSerializer(serializers.ModelSerializer):
    class Meta:
        model = topic
        fields = ['topic_name']

class TimeTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = ['time_from','time_to','day']

class LessonPlanSerializer(serializers.ModelSerializer):
    lesson_name=LessonnameSerializer()
    topic=topicnameSerializer()
    timetable=TimeTableSerializer()
    class Meta:
        model=LessonPlan
        exclude = ('session',)

class UploadContentSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    class Meta:
        model=UploadContent
        fields = '__all__'


class StaffMeetingSerializer(serializers.ModelSerializer):
    Role=StaffRoleSerializer()
    Addstaff=StaffAttendanSerializer1()
    class Meta:
        model = StaffMeeting
        fields = '__all__'


class OnlineClassSerializer(serializers.ModelSerializer):
    Role=StaffRoleSerializer()
    Addstaff=StaffAttendanSerializer1()
    Class=ClassSerializer()
    section=SectionSerializer()
    user=UserSerializer()
    class Meta:
        model = OnlineClass
        fields = '__all__'

class ParentMeetingSerializer(serializers.ModelSerializer):
    Addstaff=StaffAttendanSerializer1()
    Class=ClassSerializer()
    section=SectionSerializer()
    user=UserSerializer()
    StudentAdmission=StudentAdmissionSerializer()
    class Meta:
        model = ParentMeeting
        fields = '__all__'


class ParentMeetingNoteSerializer(serializers.ModelSerializer):
    parentmeeting=ParentMeetingSerializer()
    user=UserSerializer()
    class Meta:
        model = ParentMeetingNote
        fields = '__all__'

class StudentmeetingnoteSerializer(serializers.ModelSerializer):
    parentmeeting=ParentMeetingSerializer()
    onlinemeeting=OnlineClassSerializer()
    user=UserSerializer()
    class Meta:
        model = Studentmeetingnote
        fields = '__all__'

class StaffMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffMeeting
        fields = '__all__'

class OnlineClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineClass
        fields = '__all__'

class ParentMeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentMeeting
        fields = '__all__'
class AddStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddStaff
        fields = ['roles']

class StudentAdmissionmeetSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = ['first_name']

class ClassNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=Class
        fields='__all__'

class SectionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'

class SubjectsnnamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = '__all__'

class SubjectGroupnamesSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubjectGroup
        fields = '__all__'

class AssignClassTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssignClassTeacher
        fields = '__all__'

class TimeTableNameSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = '__all__'

class AddStaffNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddStaff
        fields='__all__'

class DesignMarkSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model=DesignMarkSheet
        fields='__all__'

class AdmitCardSerializer(serializers.ModelSerializer):
    class Meta:
        model=AdmitCard
        fields='__all__'


class AdmitCardNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdmitCard
        fields='__all__'

class AddExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddExam
        fields='__all__'

class EntryMarksSerializer(serializers.ModelSerializer):

    class Meta:
        model = EntryMarks
        fields='__all__'

class PromoteStudentSerializer(serializers.ModelSerializer):
    student=StudentAdmissionSerializer()
    Class=ClassSerializer()
    section=SectionSerializer()

    class Meta:
        model=PromoteStudent
        fields='__all__'

class PromoteStudentNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromoteStudent
        fields='__all__'

class TimeTabledtuSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeTable
        fields = '__all__'

class ExamStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamStudent
        fields = '__all__'

class AddExamSubjectSerializer(serializers.ModelSerializer):
    exam=AddExamSerializer()
    subject=SubjectsSerializer()
    class Meta:
        model = AddExamSubject
        fields = '__all__'

# 17 October

class FeesTypeDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesTypeDiscount
        fields = '__all__'

class FeesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesType
        fields = '__all__'

class FeesGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesGroup
        fields = '__all__'

class FeesMasterSerializer(serializers.ModelSerializer):
    fees_group=FeesGroupSerializer()
    fees_type=FeesTypeSerializer()
    class Meta:
        model = FeesMaster
        fields = '__all__'

class FeesTypeDiscountstuSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeesTypeDiscount
        fields = ['fees_type']

class FeesAssignSerializer(serializers.ModelSerializer):
    student=StudentAdmissionSerializer()
    fees=FeesMasterSerializer()
    class Meta:
        model = FeesAssign
        fields = '__all__'

class DiscountAssignSerializer(serializers.ModelSerializer):
    student=StudentAdmissionSerializer()
    discount=FeesTypeDiscountstuSerializer()
    fees=FeesAssignSerializer()

    class Meta:
        model = DiscountAssign
        fields = '__all__'

# 18 october

class AddLeaveTypeNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddLeaveType
        fields = '__all__'

class ApproveLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model=ApproveLeave
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields = '__all__'

class AddStaffdisableSerializer(serializers.ModelSerializer):
    class Meta:
        model=AddStaff
        fields = '__all__'

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Designation
        fields = '__all__'

# 23 october
class StudentAdmissionprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = '__all__'

class StudentAdmissionstudisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = '__all__'

class StudentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCategory
        fields = '__all__'


class StudentAdmissionstudisSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = '__all__'

class StudentAdmissionprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = '__all__'



class DisableReasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisableReason
        fields = '__all__'

class StudentAdmissionaddSerializer(serializers.ModelSerializer):
    Class=ClassSerializer()
    section=SectionSerializer()
    category=StudentCategorySerializer()
    # student_house=StudentHouseSerializer()
    vehicle_number=VehicleSerializer()
    route_list=RountSerializer()
    hostel=RountSerializer()
    room_number=HostelRoomSerializer()
    diable_reson=DisableReasonSerializer()
    user_student=UserSerializer()
    user_parent=UserSerializer()
    created_by=UserSerializer()
    class Meta:
        model = StudentAdmission

        exclude = ('session',)
        
        
class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'        
        
        
        
class SchoolRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolRegistration
        fields = '__all__'             



