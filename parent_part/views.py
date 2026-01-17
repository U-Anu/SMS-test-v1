from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from parent_part.models import *
from parent_part.forms import *
from sub_part.models import *
from sub_part.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from django.http import JsonResponse
from sub_part.views import get_week_dates
from payment.mpesa_payments import *
from sub_part.decorators import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Create your views here.
def signup(request):
    return render(request,'Parent_part/parent_dashboard.html')

@login_required
@user_type_required('Parent')
def parent_dashboard(request):
    try:
        branch_name = request.session.get('branch_id', None)
        print("branch_name+++",branch_name)
        if branch_name:        
            branch_id = branch_name     
            print("branch_name==if",branch_name)  
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        student=StudentAdmission.objects.get(id=request.parent.id)
        branch = student.branch.id 
        print("branch+++",branch)
        request.session['branch_id'] = branch
        print("request.session",request.session['branch_id'])
        records=Timeline.objects.filter(branch=branch_id)
        reason=DisableReason.objects.filter(branch=branch_id)
        form=TimelineForm()
        if request.method=='POST':
            form=TimelineForm(request.POST)
            if form.is_valid():
                obj=form.save()
                obj.branch_id = branch
                obj.save()  
                return HttpResponseRedirect('/parent/student_dashboard')
            else:
                print(form.errors)
        context={
            'form':form,'records':records,'parent_dashboard':'active','student':student,'reason':reason
                }
        return render(request,'Parent_part/parent_dashboard.html',context)
    except Exception as error:
                return render(request, "error.html", {"error": error})

@login_required
@user_type_required('Parent')
def hostel_room(request):
    try:
        branch_name = request.session.get('branch_id', None)
        print("branch_name+++",branch_name)
        if branch_name:        
            branch_id = branch_name     
            print("branch_name==if",branch_name)  
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        records=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
        hostel_records=HostelRoom.objects.filter(id=records.route_list.id) if records.route_list else None
        context={
        'hostel_room':'active','record':records,"hostel_records":hostel_records
                }
        return render(request,'Parent_part/hostel_room.html',context)
    except Exception as error:
                return render(request, "error.html", {"error": error})

@login_required
@user_type_required('Parent')
def transport_routes(request):
    try:
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        records=AssignVehicle.objects.filter(branch=branch_id)
        record=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
        assign_vehicle=AssignVehicle.objects.filter(id=record.vehicle_number.id) if record.vehicle_number else None
        print("assign_vehicle===",assign_vehicle)
        context={
        'records':records,'transport_routes':'active','record':record,"assign_vehicle":assign_vehicle
                }
        return render(request,'Parent_part/transport_routes.html',context)
    except Exception as error:
                return render(request, "error.html", {"error": error})

@login_required
@user_type_required('Parent')
def books(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    records =AddBook.objects.filter(branch=branch_id)
    context={
        'records':records,'books':'active',
            }
    return render(request,'Parent_part/books.html',context)

@login_required
@user_type_required('Parent')
def books_issued(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    record=LibrayMember.objects.filter(student=request.parent.id,branch_id=branch_id).last()
    records=IssueBook.objects.filter(member=record)
    context={
        'book_issued':'active','records':records
            }
    return render(request,'Parent_part/books_issued.html',context)

@login_required
@user_type_required('Parent')
def teacher_reviews(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    student_obj=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    rating=TeacherRating.objects.filter(student=student_obj,branch_id=branch_id)
    rating_staff=[data.staff.id for data in rating]
    assign_teacher=AssignClassTeacher.objects.filter(Class=student_obj.Class,section=student_obj.section,branch_id=branch_id).last()
    records=assign_teacher.class_teacher.filter(branch=branch_id) if assign_teacher else [] 
    context={
        'teacher_reviews':'active','records':records,'rating_staff':rating_staff,'rating':rating
    }
    return render(request,'Parent_part/teacher_reviews.html',context)

@login_required 
@user_type_required('Parent')
def notice_board(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    record=noticeBoard.objects.filter(branch=branch_id)
    context={
        'notice_board_parent':'active','record':record
            }
    return render(request,'Parent_part/notice_board.html',context)

@login_required
@user_type_required('Parent')
def notice_board_view(request): 
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    records=noticeBoard.objects.filter(branch=branch_id)
    context={
        'records':records,'notice_board_view':'active'
            }
    return render(request,'Parent_part/notice_board_view.html',context)

@login_required
@user_type_required('Parent')
def attendance(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    record=StudentAttendance.objects.filter(student=request.parent.id,branch_id=branch_id)
    print("record+++",record)
    context={
        'attendance':'active','record':record
            }
    return render(request,'Parent_part/attendance.html',context)

@login_required
@user_type_required('Parent')
def apply_leave(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    class_records=Class.objects.filter(branch=branch_id)
    section_records=Section.objects.filter(branch=branch_id)
    records=Addleave.objects.filter(student=request.parent.id,branch_id=branch_id)
    student=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    form=AddleaveParentForm(initial={'Class':student.Class,'section':student.section,'student':student.id})
    if request.method=='POST':
        form=AddleaveParentForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.branch_id = branch_id
            obj.save() 
            return HttpResponseRedirect('/parent/apply_leave_parent')
        else:
            print(form.errors)
    context={
        'form':form,'records':records,'apply_leave_parent':'active','class_records':class_records,'section_records':section_records
            }
    return render(request,'Parent_part/apply_leave.html',context)

@login_required
@user_type_required('Parent')
def apply_leave_edit(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)

    records=Addleave.objects.filter(student=request.parent.id,branch_id=branch_id)
    record=Addleave.objects.get(id=pk)
    data_branch_id = record.branch.id
    form=AddleaveParentForm(instance=record)
    if request.method=='POST':
        form=AddleaveParentForm(request.POST,instance=record)
        if form.is_valid():
            if branch_id == data_branch_id:
                form.save()
            else:
                form.instance.branch_id = branch_id
            form.save()
            return HttpResponseRedirect('/parent/apply_leave_parent')
    context={
        'form':form,'records':records,'apply_leave':'active'
            }
    return render(request,'Parent_part/apply_leave_edit.html',context)

@login_required
@user_type_required('Parent')
def apply_leave_delete(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    add_leave=Addleave.objects.get(id=pk)
    add_leave_branch_id = add_leave.branch.id
    if int(add_leave_branch_id) == int(branch_id):                        
        Addleave.objects.get(id=pk).delete()
    else:
        messages.error(request, "School id Doesn't match record no delete")
    return HttpResponseRedirect('/parent/apply_leave_parent')

@login_required
@user_type_required('Parent')
def online_exam(request):
    context={
        'online_exam':'active'
    }
    return render(request,'Parent_part/online_exam.html',context)

@login_required
@user_type_required('Parent')
def homework(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=AssingHomeWork.objects.filter(student=request.parent.id,branch_id=branch_id)
    if request.method=='POST':
        obj=records.get(id=request.POST.get('id'))
        obj.message=request.POST.get('message')
        obj.document=request.FILES.get('document')
        obj.branch_id=branch_id
        obj.save()
        return redirect('homework')
    context={
        'records':records,'homework':'active'
            }
    return render(request,'Parent_part/homework.html',context)


@login_required
@user_type_required('Parent')
def homework_view(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=AddHomeWork.objects.filter(branch=branch_id)
    record=AddHomeWork.objects.get(id=pk,branch_id=branch_id)
    # print('form',form)
    context={
        'record':record,'records':records,'homework':'active'
            }
    return render(request,'Parent_part/homework_view.html',context)

# Download center

@login_required
@user_type_required('Parent')
def assignment_list(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='assignments',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
        'assignment_list':'active','records':records
    }
    return render(request,'Parent_part/assignment_list.html',context)

@login_required
@user_type_required('Parent')
def study_material(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='study_material',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
         'study_material':'active','records':records,
    }
    return render(request,'Parent_part/study_material.html',context)

@login_required
@user_type_required('Parent')
def syllabus(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='syllabus',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
         'syllabus':'active','records':records,
    }
    return render(request,'Parent_part/syllabus.html',context)

@login_required
@user_type_required('Parent')
def other_download_list(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='other_download',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
         'other_download_list':'active','records':records,
    }
    return render(request,'Parent_part/other_download_list.html',context)

@login_required
@user_type_required('Parent')
def exam_schedule(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=ExamStudent.objects.filter(student=request.parent.id,branch_id=branch_id)
    context={
        'records':records,'exam_schedule':'active'
            }
    return render(request,'Parent_part/exam_schedule.html',context)

@login_required
@user_type_required('Parent')
def exams_view(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=AddExamSubject.objects.filter(exam=pk,branch_id=branch_id)
    context={
        'records':records,'exam_schedule':'active'
            }
    return render(request,'Parent_part/exams_view.html',context)

@login_required
@user_type_required('Parent')
def exam_result(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=ExamStudent.objects.filter(student=request.parent.id,branch_id=branch_id)
    context={
        'records':records,'exam_result':'active'
            }
    return render(request,'Parent_part/exam_result.html',context)

@login_required
@user_type_required('Parent')
def exam_result_view(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=EntryMarks.objects.filter(exam=pk,branch_id=branch_id)
    context={
        'records':records,'exam_result':'active'
            }
    return render(request,'Parent_part/exam_result_view.html',context)

@login_required
@user_type_required('Parent')
def class_timetable(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session,branch_id=branch_id)

    context={
        'TimeTable_records':TimeTable_records,'class_timetable':'active'
            }
    return render(request,'Parent_part/class_timetable.html',context)

@login_required
@user_type_required('Parent')
def lesson_plan(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session,branch_id=branch_id)
    if request.method=='POST':
        week=request.POST.get('week_days')
        week_split=week.split('-')
        year = int(week_split[0])
        week_number = int(week_split[1][1:])
        dates_in_week = get_week_dates(year, week_number)
        TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session)
        week_days=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        Monday=[]
        Tuesday=[]
        Wednesday=[]
        Thursday=[]
        Friday=[]
        Saturday=[]
        Sunday=[]
        week_no=0
        for days in week_days:

            time_table_record=TimeTable_records.filter(day = days)
            for data in time_table_record:
                lesson_plan=LessonPlan.objects.filter(time_table=data,date=dates_in_week[week_no].date()).last()
                if week_no == 0:
                    if lesson_plan:
                        Monday.append(['Edit',lesson_plan])
                elif week_no==1:
                    if lesson_plan:
                        Tuesday.append(['Edit',lesson_plan])
                elif week_no==2:
                    if lesson_plan:
                        Wednesday.append(['Edit',lesson_plan])
                elif week_no==3:
                    if lesson_plan:
                        Thursday.append(['Edit',lesson_plan])
                elif week_no==4:
                    if lesson_plan:
                        Friday.append(['Edit',lesson_plan])
                elif week_no==5:
                    if lesson_plan:
                        Saturday.append(['Edit',lesson_plan])
                elif week_no==6:
                    if lesson_plan:
                        Sunday.append(['Edit',lesson_plan])
            week_no+=1
        print(Monday,Tuesday)
        context={
            'lesson_plan_parent':'active','Monday':Monday,'Tuesday':Tuesday,'Wednesday':Wednesday,'Thursday':Thursday,'Friday':Friday,'Saturday':Saturday,'Sunday':Sunday,
            'dates_in_week':dates_in_week,'week':week
                }
        return render(request,'Parent_part/lesson_plan.html',context)
    context={
        'lesson_plan_parent':'active'
            }
    return render(request,'Parent_part/lesson_plan.html',context)

@login_required
@user_type_required('Parent')
def syllabus_status(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    classs=student.Class
    section=student.section
    subject=SubjectGroup.objects.filter(Class=student.Class,section=student.section,branch_id=branch_id).last()
    records=[]
    chart_percent=[]
    if subject:
        for sub in subject.subject.filter(branch=branch_id):
            subj={}
            lesson_records=Lesson.objects.filter(Class_id=classs,section_id=section,subject=sub.id,branch_id=branch_id)
            record=[]
            total=0
            percent=1
            for data in lesson_records:
                dict={}
                topic_records=topic.objects.filter(lesson_name=data.id)
                if topic_records.count() > 0 :
                    percentage=int(topic_records.filter(status="complete").count() * 100 / topic_records.count())
                    percent*=percentage/100
                    total+=1
                    dict['percentage']=f'{percentage}% Complete'
                else:
                    dict['percentage']='No Status'
                dict['lesson']=data
                dict['topic']=topic_records
                record.append(dict)
            if total > 0:
                chart_percent.append([percent*100,sub.subject_name])
                subj['percentage']=f'{percent*100}% Complete'
            else:
                chart_percent.append([0,sub.subject_name])
                subj['percentage']='0% Complete'
            subj['subject']=sub
            subj['record']=record
            records.append(subj)
        else:
            records=[]
    context={
        'syllabus_status_parent':'active','records':records,'chart_percent':chart_percent
    }
    return render(request, 'Parent_part/syllabus_status.html', context)

@login_required
@user_type_required('Parent')
def parent_meeting(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    section_record=Section.objects.filter(branch=branch_id)
    class_record=Class.objects.filter(branch=branch_id)
    addstaff=AddStaff.objects.filter(branch=branch_id)
    addstudent=StudentAdmission.objects.filter(branch=branch_id)
    records = ParentMeeting.objects.filter(branch=branch_id)
    form1=StudentAdmissionForm()

    if request.method == 'POST':
        form = ParentMeetingForm(request.POST)
        if form.is_valid():
            form.save()

            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.branch_id = branch_id
            obj.save()
            return redirect('/parent_meeting')
    else:
        form = ParentMeetingForm()
        print(form.errors)
    context = {
        'records': records,
        'form': form,
        'form1': form1,
        'parent_meeting':'active',
        'addstaff':addstaff,
        'section_record':section_record,
        'addstudent':addstudent,
        'class_record':class_record,
    }

    return render(request, 'Parent_part/parent_meeting.html', context)

@login_required
@user_type_required('Parent')
def parent_meeting_feeedback(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        records=ParentMeeting.objects.filter(branch=branch_id)
        form=ParentMeetingNoteForm ()
        record=ParentMeeting.objects.get(id=pk)
        data_branch_id = record.branch.id
        if request.method=='POST':
            form=StaffMeetingForm(request.POST)
            if form.is_valid():
                if branch_id == data_branch_id:
                    form.save()
                else:
                    form.instance.branch_id = branch_id
                form.save()
            return HttpResponseRedirect('/parent/parent_meeting')

        context={
            'form':form,'records':records,'online_class':'active','record':record,
                }
        return render(request,'Parent_part/parent_meeting_feeedback.html',context)

@login_required
@user_type_required('Parent')
def parent_meeting_view(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        records=ParentMeeting.objects.filter(branch=branch_id)
        form=ParentMeetingNoteForm ()
        record=ParentMeeting.objects.get(id=pk,branch_id=branch_id) 
        context={
            'form':form,'records':records,'staff_meeting':'active','record':record,
                }
        return render(request,'Parent_part/parent_meeting_view.html',context)

@login_required
@user_type_required('Parent')
def fees_parent(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    toady_date=datetime.now().date()
    records=StudentAdmission.objects.get(id=request.parent.id,branch_id=branch_id)
    fees_records=FeesAssign.objects.filter(student_id=request.parent.id,branch_id=branch_id)
    # fees_discount=FeesTypeDiscount.objects.filter(branch=branch_id)
    fees_discount=DiscountAssign.objects.filter(student=request.parent.id,branch_id=branch_id)
    paid_record=StudentFess.objects.filter(student=request.parent.id,branch_id=branch_id)
    print("paid_record---",paid_record)
    # payment = mpesa_stk_push(1, 254711849456, 'karan')
    # print('payment==',payment)
    
    context={
        'records':records,'fees_records':fees_records,'toady_date':toady_date,'fees_discount':fees_discount,
        'paid_record':paid_record,'fees_parent':'active'
    }
    return render(request,'Parent_part/fees_parent.html',context)

@login_required
@user_type_required('Parent')
def chat_index(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    staff_records=AddStaff.objects.filter(branch=branch_id)
    student_records=StudentAdmission.objects.filter(branch=branch_id)
    contact_record = AddContact.objects.filter(user=request.user,branch_id=branch_id)
    records=[]
    for data in contact_record:
        dict={}
        count=ContanctMessage.objects.filter(status='sended',contact=data).count()
        dict['obj']=data
        dict['unread_count']=count
        records.append(dict)
    context={
        'staff_records':staff_records,'student_records':student_records,'contact_record':contact_record,'records':records
            }
    return render(request,'Chat/chat_index_parent.html',context)

@login_required
@user_type_required('Parent')
def save_contact(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    usertype= request.POST.get('usertype')
    user_id= request.POST.get('user_id')
    if usertype == 'Staff':
        staff_obj=AddStaff.objects.get(id=user_id,branch_id=branch_id)
        AddContact.objects.get_or_create(
            user=request.user,
            staff_id=user_id,
            contact_user=staff_obj.user,
            usertype=usertype,
            branch_id=branch_id
        )
        AddContact.objects.get_or_create(
            user=staff_obj.user,
            staff_id=user_id,
            contact_user=request.user,
            usertype='Parent',
            branch_id=branch_id
        )
    else:
        if usertype == 'Student':
            user_obj = StudentAdmission.objects.get(id=user_id,branch_id=branch_id)
            user_obj_id=user_obj.user_student
        elif usertype == 'Parent':
            user_obj = StudentAdmission.objects.get(id=user_id,branch_id=branch_id)
            user_obj_id=user_obj.user_parent
        print('===',user_obj_id)
        AddContact.objects.get_or_create(
            user=request.user,
            student_id=user_id,
            contact_user=user_obj_id,
            usertype=usertype,
            branch_id=branch_id
        )
        AddContact.objects.get_or_create(
            user=user_obj_id,
            student_id=user_id,
            contact_user=request.user,
            usertype='Parent',
            branch_id=branch_id
        )
    return redirect('chat_index')

@login_required
@user_type_required('Parent')
def chat(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    staff_records=AddStaff.objects.filter(branch=branch_id)
    student_records=StudentAdmission.objects.filter(branch=branch_id)
    contact_record = AddContact.objects.filter(user=request.user,branch_id=branch_id)
    contact_obj= AddContact.objects.get(id=pk,branch_id=branch_id)
    message_records= ContanctMessage.objects.filter(contact=contact_obj,branch_id=branch_id)
    message_records.filter(status='sended').update(status='readed')
    records=[]
    for data in contact_record:
        dict={}
        count=ContanctMessage.objects.filter(status='sended',contact=data).count()
        dict['obj']=data
        dict['unread_count']=count
        records.append(dict)
    context={
        'staff_records':staff_records,'student_records':student_records,'contact_record':contact_record,
        'contact_obj':contact_obj,'pk':int(pk),'message_records':message_records,'records':records
            }
    return render(request,'Chat/chat_parent.html',context)


