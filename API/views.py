from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from sub_part.models import *
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from SchoolManagement import utils as utils_response

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions

from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class StudentAdmissionView(ListCreateAPIView):
    queryset=StudentAdmission.objects.all()
    serializer_class=StudentAdmissionSerializer

from rest_framework.decorators import api_view

@api_view(['GET'])
def student_get(request):
    if request.method=='GET':
        records=StudentAdmission.objects.all()
        serializer=StudentAdmissionSerializer(records,many=True)

    return Response(utils_response.success_response(data=serializer.data,status_code=status.HTTP_200_OK))

@api_view(['GET'])
def staff_get(request):
    if request.method=='GET':
        records=AddStaff.objects.all()
        serializer=AddStaffSerializer(records,many=True)
    return Response(utils_response.success_response(data=serializer.data,status_code=status.HTTP_200_OK))



def exception_handle_all(exception_handle):
    message = {"error": f"""{exception_handle}"""}
    print("message ", message)
    return message


class StudentAdmissionApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        records=StudentAdmission.objects.filter(user_student=request.user,session=request.Session).first()
        if not records:
            records=StudentAdmission.objects.filter(user_student=request.user,session__lt=request.Session).last()
        serializer=StudentAdmissionSerializer(records)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class UserTypeApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response(data={'user_type' : request.user.user_type }, status=status.HTTP_200_OK)


def student_object(request):
    if request.user.user_type=='Student':
        student_obj=StudentAdmission.objects.filter(user_student=request.user).last()
        student_obj=StudentAdmission.objects.filter(user_student=request.user,session=request.Session).first()
        if not student_obj:
            student_obj=StudentAdmission.objects.filter(user_student=request.user,session__lt=request.Session).last()
    elif request.user.user_type=='Parent':
        student_obj=StudentAdmission.objects.filter(user_parent=request.user).last()
    else:
        message = {
            "error": "unmatched trustee id and group"
        }
        return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

    return student_obj


class HomeWorkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=AssingHomeWork.objects.filter(student=obj.id)

        serializer=AssingHomeWorkSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        try:
            serializer = HomeWorkSerializer(data=request.data)
            if serializer.is_valid():
                print('serializer',serializer)
                id = serializer.data.get("homework_id")
                message = serializer.data.get("message")
                attach_document1 = serializer.validated_data.get("attach_document")
                obj=AssingHomeWork.objects.filter(id=id).last()
                if obj:
                    obj.message=message
                    obj.document=attach_document1
                    obj.save()
                    success_message = {"status": "Home Work Submitted Successfully."}
                    print("Thanks1")
                    return Response(data=success_message, status=status.HTTP_200_OK)
                else:
                    success_message = {"status": "Homework dosn't exist."}
                    print("fail")
                    return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class AttendanceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=StudentAttendance.objects.filter(student=obj.id)
        serializer=StudentAttendanceSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AddHomeWorkListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = AddHomeWork.objects.all()
        serializer = ViewHomeWorkSerializer(homework, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddHomeWorkSerializer(data=request.data)
        if serializer.is_valid():
            homework=serializer.save(created_by=request.user)
            student=StudentAdmission.objects.filter(Class=request.POST.get('Class'),
                                                    section=request.POST.get('section'),session=request.Session)
            for data in student:
                AssingHomeWork.objects.get_or_create(
                    home_work_id=homework.pk,
                    student_id=data.id,
                    status='Pending'
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddHomeWorkDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return AddHomeWork.objects.get(pk=pk)
        except AddHomeWork.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        homework = self.get_object(pk)
        serializer = ViewHomeWorkSerializer(homework)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            homework = self.get_object(pk)
            serializer = AddHomeWorkSerializer(homework, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            homework = self.get_object(pk)
            homework.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class ClassListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        classes = Class.objects.all()
        serializer = ClassIDSerializer(classes, many=True)
        return Response(serializer.data)

class SectionsByClassView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, class_id):
        try:
            class_instance = Class.objects.get(id=class_id)
            sections = class_instance.section.all()
            serializer = SectionIDSerializer(sections, many=True)
            return Response(serializer.data)
        except Class.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

class SubjectGroupByClassAndSectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, class_id, section_id):
        try:
            subject_groups = SubjectGroup.objects.filter(Class=class_id, section=section_id)
            serializer = SubjectGroupSerializer(subject_groups, many=True)
            return Response(serializer.data)
        except SubjectGroup.DoesNotExist:
            return Response({"error": "Subject groups not found"}, status=404)

class SubjectGroupByClassAndSectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, class_id, section_id):
        try:
            subject_groups = SubjectGroup.objects.filter(Class=class_id, section=section_id)
            serializer = SubjectGroupSerializer(subject_groups, many=True)
            return Response(serializer.data)
        except SubjectGroup.DoesNotExist:
            return Response({"error": "Subject groups not found"}, status=404)

class SubjectBySubjectGroupClassView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, sub_group_id):
        try:
            subject_group_instance = SubjectGroup.objects.get(id=sub_group_id)
            subjects = subject_group_instance.subject.all()
            serializer = SubjectIDSerializer(subjects, many=True)
            return Response(serializer.data)
        except SubjectGroup.DoesNotExist:
            return Response({"error": "subject group not found"}, status=404)


class StudentLeaveListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = Addleave.objects.all()
        serializer = ViewleaveSerializer(homework, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AddleaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentByClassandSectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, class_id, section_id):
        try:
            student = StudentAdmission.objects.filter(Class=class_id,section=section_id,session=request.Session)
            serializer = StudentAdmissionSerializer(student, many=True)
            return Response(serializer.data)
        except StudentAdmission.DoesNotExist:
            return Response({"error": "Students not found"}, status=404)

class AddleaveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=Addleave.objects.filter(student=obj.id)

        serializer=AddleaveSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AvailableLeaveListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff=AddStaff.objects.get(user=request.user)
        leaves = StaffLeave.objects.filter(staff=staff)
        leave=AvailableLeave.objects.filter(staff_leave__in=leaves.values('id'),session=request.Session,available_leave__gt=0)
        print('leave',leave)
        serializer = AvailableLeaveSerializer(leave, many=True)
        return Response(serializer.data)

class StaffLeaveListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff=AddStaff.objects.get(user=request.user)
        homework = ApproveLeave.objects.filter(name=staff)
        serializer = StaffLeaveViewSerializer(homework, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffLeaveAddSerializer(data=request.data)
        if serializer.is_valid():
            staff=AddStaff.objects.get(user=request.user)
            leaves = StaffLeave.objects.filter(staff=staff)
            available_leaves=AvailableLeave.objects.filter(staff_leave__in=leaves.values('id'),session=request.Session)
            if not available_leaves:
                for data in leaves:
                    AvailableLeave.objects.get_or_create(
                        staff_leave=data,
                        available_leave=data.total_leave,
                        total_leave=data.total_leave,
                        session=request.Session
                    )
            approval_leaves=ApproveLeave.objects.filter(name=staff)
            if request.method == 'POST':
                lop=request.POST.get('lop')
                dates_str=request.POST.get('leave_dates')
                leave_dates=dates_str.split(', ')
                leave_type=request.POST.get('available_leave')
                if lop:
                    lop=int(lop)
                    leave_days=len(leave_dates)-lop
                    if leave_type:
                        lop_dates=leave_dates[leave_days:]
                    else:
                        lop_dates=leave_dates
                else:
                    leave_days=len(leave_dates)
                    lop_dates=[]

                ApproveLeave.objects.create(
                    role=staff.roles,
                    name=staff,
                    apply_date=request.POST.get('apply_date'),
                    leave_type_id=request.POST.get('leave_type'),
                    leave_dates=leave_dates[:leave_days],
                    number_of_days=leave_days,
                    LOP_leave_dates=lop_dates,
                    LOP_number_of_days=lop,
                    reason=request.POST.get('reason'),
                    note=' ',
                    attach_document=request.FILES.get('document'),
                    status='Pending',
                    created_by=request.user
                )
                available_leave=AvailableLeave.objects.filter(staff_leave__leave_type=request.POST.get('leave_type'),session=request.Session).last()
                available_leave.available_leave=available_leave.available_leave-leave_days
                available_leave.save()
            # serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RountCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        route = Route.objects.all()
        serializer = RountSerializer(route, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = RountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Vehiclecreateview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        hostel = Vehicle.objects.all()
        serializer = VehicleSerializer(hostel, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = VehicleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class AssignVehiclecreateview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        assign_vechicle = AssignVehicle.objects.all()

        serializer = AssignVehiclSerializer(assign_vechicle, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AssignVehiclSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Rountlistcreateview(APIView):
    def get(self, request):
        assign_vechicle = Route.objects.all()
        serializer = RountSerializer1(assign_vechicle, many=True)
        return Response(serializer.data)


class Vehiclelistcreateview(APIView):
    def get(self, request):
        assign_vechicle = Vehicle.objects.all()
        serializer = VehicleSerializer1(assign_vechicle, many=True)
        return Response(serializer.data)

class StaffRoleview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        roles = Role.objects.all()
        serializer = StaffRoleSerializer(roles, many=True)
        return Response(serializer.data)



class StaffAttendanview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff=AddStaff.objects.get(user=request.user)
        records=StaffAttendance.objects.filter(staff=staff)
        serializer = StaffAttendanceSerializer(records, many=True)
        return Response(serializer.data)


class StudenceAttendanview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        Students=StudentAdmission.objects.get(user_student=request.user)
        records=StudentAttendance.objects.filter(student=Students)
        serializer = StudentAttendanceSerializer(records, many=True)
        return Response(serializer.data)

class StudenceAttendanlistview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return StudentAdmission.objects.get(pk=pk)
        except StudentAdmission.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        stdents = self.get_object(pk)
        serializer = StudentAdmissionSerializer(stdents)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            stdents = self.get_object(pk)
            serializer = AddleaveSerializer(stdents, data=request.data)
            if serializer.status == 'disapprove':
                serializer.status = 'approve'
                serializer.approved_by = request.user
            elif serializer.status == 'approve':
                serializer.status = 'disapprove'
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Hostelcreateview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        hostel = Hostel.objects.all()
        serializer = HostelSerializer(hostel, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = HostelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class RoomTypecreateview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        hostel = RoomType.objects.all()
        serializer = RoomTypeSerializer(hostel, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = RoomTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class HostelRoomcreateview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        hostel = HostelRoom.objects.all()
        serializer = HostelRoomSerializer(hostel, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = HostelRoomSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class StudentHostelview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=StudentAdmission.objects.filter(hostel=obj.id)

        serializer=StudentHostelSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Routeview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        route = Route.objects.all()
        serializer = RountSerializer(route, many=True)
        return Response(serializer.data)

class Vehicleview(APIView):

    def get(self, request):
        route = Vehicle.objects.all()
        serializer = VehicleSerializer(route, many=True)
        return Response(serializer.data)

class StudentAdmissionHostelview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = StudentAdmission.objects.all()
        serializer = StudentAdmissionHostelSerializer(stu_hostel, many=True)
        return Response(serializer.data)

class StudentAdmissionuserview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = StudentAdmission.objects.all()
        serializer = StudentAttendanceSerializer1(stu_hostel, many=True)
        return Response(serializer.data)

class StaffAttendanuserview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = StaffAttendance.objects.all()
        serializer = StudentAttendanceSerializer1(stu_hostel, many=True)
        return Response(serializer.data)
class Hostelview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = Hostel.objects.all()
        serializer = HostelSerializer1(stu_hostel, many=True)
        return Response(serializer.data)

class RoomTypeview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_room = RoomType.objects.all()
        serializer = RoomTypeSerializer1(stu_room, many=True)
        return Response(serializer.data)

class Lessonview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lesson = Lesson.objects.all()
        serializer = LessonSerializer(lesson, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = LessonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class Subjectsview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        subject_name = Subjects.objects.all()
        serializer = SubjectsnameSerializer(subject_name, many=True)
        return Response(serializer.data)

class Lessonnameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_lesson = Lesson.objects.all()
        serializer = LessonnameSerializer(stu_lesson, many=True)
        return Response(serializer.data)

class topicview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        topics = topic.objects.all()
        serializer = topicSerializer(topics, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = topicSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class StudentLessonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=LessonPlan.objects.filter(created_by=obj.id)
        serializer=LessonPlanSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class LessonPlanView(APIView):

    def get(self, request):
        lesson_plam = LessonPlan.objects.all()
        serializer = LessonPlanSerializer(lesson_plam, many=True)
        return Response(serializer.data)

class topinamecview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lesson_plam = topic.objects.all()
        serializer = topicnameSerializer(lesson_plam, many=True)
        return Response(serializer.data)

class timetablecview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lesson_plam = TimeTable.objects.all()
        serializer = TimeTableSerializer(lesson_plam, many=True)
        return Response(serializer.data)


class Assignmentsview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        stu_assigment=StudentAdmission.objects.get(id=obj.id)
        records1=UploadContent.objects.filter(Class_id=stu_assigment.Class,section_id=stu_assigment.section,content_type='assignments')
        records2=UploadContent.objects.filter(Class_id__isnull=True)
        records=records1 | records2
        serializer=UploadContentSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class studymaterialview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        stu_assigment=StudentAdmission.objects.get(id=obj.id)
        records1=UploadContent.objects.filter(Class_id=stu_assigment.Class,section_id=stu_assigment.section,content_type='study_material')
        records2=UploadContent.objects.filter(Class_id__isnull=True)
        records=records1 | records2
        serializer=UploadContentSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class syllabusview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        stu_assigment=StudentAdmission.objects.get(id=obj.id)
        records1=UploadContent.objects.filter(Class_id=stu_assigment.Class,section_id=stu_assigment.section,content_type='syllabus')
        records2=UploadContent.objects.filter(Class_id__isnull=True)
        records=records1 | records2
        serializer=UploadContentSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class otherdownloadview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        stu_assigment=StudentAdmission.objects.get(id=obj.id)
        records1=UploadContent.objects.filter(Class_id=stu_assigment.Class,section_id=stu_assigment.section,content_type='other_download')
        records2=UploadContent.objects.filter(Class_id__isnull=True)
        records=records1 | records2
        serializer=UploadContentSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class uploadcontentview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        lesson_plam = UploadContent.objects.all()
        serializer = UploadContentSerializer(lesson_plam, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UploadContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffMeetingview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff_meet = StaffMeeting.objects.all()
        serializer = StaffMeetingSerializer(staff_meet, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StaffMeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ParentMeetingview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff_meet = ParentMeeting.objects.all()
        serializer = ParentMeetingSerializer(staff_meet, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ParentMeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OnlineClassview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff_meet = OnlineClass.objects.all()
        serializer = OnlineClassSerializer(staff_meet, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OnlineClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user,session=request.Session)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddStaffview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = AddStaff.objects.all()
        serializer = AddStaffSerializer(homework, many=True)
        return Response(serializer.data)

class StudentAdmissionmeetingview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = StudentAdmission.objects.all()
        serializer = StudentAdmissionmeetSerializer(stu_hostel, many=True)
        return Response(serializer.data)

class Classview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_class = Class.objects.all()
        serializer = ClassNameSerializer(stu_class, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = VehicleSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Sectionview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_section = Section.objects.all()
        serializer = SectionNameSerializer(stu_section, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SectionNameSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Subjectsnameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_subject = Subjects.objects.all()
        serializer = SubjectsnnamesSerializer(stu_subject, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SubjectsnnamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class SubjectGroupnameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_subjectgroup = SubjectGroup.objects.all()
        serializer = SubjectGroupnamesSerializer(stu_subjectgroup, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = SubjectGroupnamesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class AssignClassTeacherview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = AssignClassTeacher.objects.all()
        serializer = AssignClassTeacherSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AssignClassTeacherSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class TimeTableview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_tiamtable = TimeTable.objects.all()
        serializer = TimeTableNameSerializer(stu_tiamtable, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = TimeTableNameSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class AddStaffnameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_hostel = AddStaff.objects.all()
        serializer = AddStaffNameSerializer(stu_hostel, many=True)
        return Response(serializer.data)



class DesignMarkSheetview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = DesignMarkSheet.objects.all()
        serializer = DesignMarkSheetSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = DesignMarkSheetSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class AdmitCardview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = AdmitCard.objects.all()
        serializer = AdmitCardSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AdmitCardSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class AdmitCardNameview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return AdmitCard.objects.get(pk=pk)
        except AdmitCard.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        homework = self.get_object(pk)
        serializer = AdmitCardSerializer(homework)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            homework = self.get_object(pk)
            serializer = AdmitCardNameSerializer(homework, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class AddExamview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = AddExam.objects.all()
        serializer = AddExamSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AddExamSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class EntryMarksview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = EntryMarks.objects.all()
        serializer = EntryMarksSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

class PromoteStudentview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = PromoteStudent.objects.all()
        serializer = PromoteStudentSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

class PromoteStudentNameview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return PromoteStudent.objects.get(pk=pk)
        except PromoteStudent.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        homework = self.get_object(pk)
        serializer = PromoteStudentNameSerializer(homework)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            homework = self.get_object(pk)
            serializer = PromoteStudentSerializer(homework, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class TimeTableStudentview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

        students=StudentAdmission.objects.get(id=obj.id)
        print('students',students)
        TimeTable_records=TimeTable.objects.filter(Class_id=students.Class,section_id=students.section)
        serializer=TimeTabledtuSerializer(TimeTable_records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class TimeTablestaffview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        staff=AddStaff.objects.get(user=request.user)
        staffTimetable = TimeTable.objects.filter(teacher=staff)
        serializer = TimeTabledtuSerializer(staffTimetable, many=True)
        return Response(serializer.data)

class AddExamSubjectview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = AddExamSubject.objects.all()
        serializer = AddExamSubjectSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AddExamSubjectSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class printadmitview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = AdmitCard.objects.all()
        serializer = AdmitCardSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

class printmarkview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_assingclass = DesignMarkSheet.objects.all()
        serializer = DesignMarkSheetSerializer(stu_assingclass, many=True)
        return Response(serializer.data)

class FeesTypeDiscountview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_FeesTypeDiscount = FeesTypeDiscount.objects.all()
        serializer = FeesTypeDiscountSerializer(stu_FeesTypeDiscount, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = FeesTypeDiscountSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class FeesTypeview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_FeesType = FeesType.objects.all()
        serializer = FeesTypeSerializer(stu_FeesType, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = FeesTypeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class FeesGroupview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_FeesGroup = FeesGroup.objects.all()
        serializer = FeesGroupSerializer(stu_FeesGroup, many=True)
        return Response(serializer.data)


class FeesMasterview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_FeesMaster = FeesMaster.objects.all()
        serializer = FeesMasterSerializer(stu_FeesMaster, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = FeesMasterSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class FeesAssignview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = FeesAssign.objects.all()
        serializer = FeesAssignSerializer(homework, many=True)
        return Response(serializer.data)


class StudentFessview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = StudentFess.objects.all()
        serializer = StudentFessSerializer(homework, many=True)
        return Response(serializer.data)

class DiscountAssignview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = DiscountAssign.objects.all()
        serializer = DiscountAssignSerializer(homework, many=True)
        return Response(serializer.data)

class FeesTypeDiscountstuview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = FeesTypeDiscount.objects.all()
        serializer = FeesTypeDiscountstuSerializer(homework, many=True)
        return Response(serializer.data)

class FeesTypeDiscountstuview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = FeesTypeDiscount.objects.all()
        serializer = FeesTypeDiscountstuSerializer(homework, many=True)
        return Response(serializer.data)

class FeesMasterstuview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = FeesMaster.objects.all()
        serializer = FeesMasterstuSerializer(homework, many=True)
        return Response(serializer.data)

class FeesTypestuview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        homework = FeesType.objects.all()
        serializer = FeesTypestuSerializer(homework, many=True)
        return Response(serializer.data)


class AddLeaveTypenamesview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_Department = AddLeaveType.objects.all()
        serializer = AddLeaveTypeSerializer(stu_Department, many=True)
        return Response(serializer.data)

class AddLeaveTypeNameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_AddLeaveType = AddLeaveType.objects.all()
        serializer = AddLeaveTypeNameSerializer(stu_AddLeaveType, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = AddLeaveTypeNameSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class ApproveLeaveNameview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = ApproveLeave.objects.all()
        serializer = ApproveLeaveSerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ApproveLeaveSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class Departmentview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_Department = Department.objects.all()
        serializer = DepartmentSerializer(stu_Department, many=True)
        return Response(serializer.data)

class AddStaffdisview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        records=AddStaff.objects.filter(status='Disable')
        if request.method=='POST':
            records=AddStaff.objects.filter(roles=request.POST.get('roles'),status='Disable')
        serializer = AddStaffdisableSerializer(records, many=True)
        return Response(serializer.data)

class Designationview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_Department = Department.objects.all()
        serializer = DesignationSerializer(stu_Department, many=True)
        return Response(serializer.data)

class Addleavestuview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=Addleave.objects.filter(student=obj.id)
        serializer=AddleaveSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

# 23 october

class StudentAdmissionStudentView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return StudentAdmission.objects.get(pk=pk)
        except StudentAdmission.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        homework = self.get_object(pk)
        serializer = StudentAdmissionprofileSerializer(homework)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            homework = self.get_object(pk)
            serializer = StudentAdmissionprofileSerializer(homework, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class StudentAdmissionstudisview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, ):
        try:
            student_disable = StudentAdmission.objects.filter(status='Disable',session=request.Session)
            serializer = StudentAdmissionstudisSerializer(student_disable, many=True)
            return Response(serializer.data)
        except StudentAdmission.DoesNotExist:
            return Response({"error": "Subject groups not found"}, status=404)


class StudentCategorystudisview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = StudentCategory.objects.all()
        serializer = StudentCategorySerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = StudentCategorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class StudentAdmissionStudentbulkView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return StudentAdmission.objects.get(pk=pk)
        except StudentAdmission.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, pk):
        homework = self.get_object(pk)
        serializer = StudentAdmissionstudisSerializer(homework)
        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            homework = self.get_object(pk)
            homework.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class Studentprofilestudisview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.user_type=='Student' or request.user.user_type=='Parent':
            obj=student_object(request)
        else:
            message = {
                "error": "Your not student or parent"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        records=StudentAdmission.objects.filter(created_by=obj.id)
        serializer=StudentAdmissionprofileSerializer(records,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class StudentAdmissionaddview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = StudentAdmission.objects.all()
        serializer = StudentAdmissionaddSerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = StudentAdmissionaddSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class StudentHouseview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = StudentHouse.objects.all()
        serializer = StudentHouseSerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = StudentHouseSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)


class DisableReasonview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = DisableReason.objects.all()
        serializer = DisableReasonSerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = DisableReasonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)

class ExamStudentview(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        stu_ApproveLeave = ExamStudent.objects.all()
        serializer = ExamStudentSerializer(stu_ApproveLeave, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        try:
            serializer = ExamStudentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "records Saves Successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(
                    data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as exception_handle:
            occur_exception = exception_handle_all(exception_handle)
            print("occur_exception ", occur_exception)
            return Response(data=occur_exception, status=status.HTTP_400_BAD_REQUEST)
        
        
class CurrencyCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serializer = CurrencySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                success_message = {"message": "Record saved successfully"}
                return Response(data=success_message, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as exception_handle:
            occur_exception = str(exception_handle)  # You can replace this with a custom function if needed
            print("occur_exception ", occur_exception)
            return Response(data={"error": occur_exception}, status=status.HTTP_400_BAD_REQUEST)  

