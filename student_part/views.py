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
from django.contrib.auth.decorators import login_required
from sub_part.views import get_week_dates
from sub_part.decorators import *
from django.contrib import messages

def signup(request):
  return render(request,'Auth/SignUp.html')

@login_required
@user_type_required('Student')
def student_dashboard(request):
    print("request.student.id+++",request.student.id)
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    if request.student is None:
        return redirect('signin')  # Replace 'signin' with the actual name of your signin URL
    else:
        # Proceed with the normal logic
        print(f"Student: {request.student}")    
    record=Studentprofileupdate.objects.filter(branch=branch_id).first()
    print('request.student.id',request.student)   
    student=StudentAdmission.objects.get(id=request.student.id)
    print("student----",student)    
    branch = student.branch.id
    request.session['branch_id'] = branch
    print("request.session",request.session['branch_id'])
    print('requestbranch',branch)
    records=Timeline.objects.filter(branch=branch_id)
    reason=DisableReason.objects.filter(branch=branch_id)
    form=TimelineForm()
    if request.method=='POST':
        form=TimelineForm(request.POST)
        if form.is_valid():
            obj=form.save()
            obj.branch_id = branch
            obj.save()
            return HttpResponseRedirect('/student_dashboard')
        else:
            print(form.errors)
    context={
        'form':form,'records':records,'student_dashboard':'active',
        'record':record,'student':student,'reason':reason
            }
    return render(request,'Student_part/student_dashboard.html',context)
@login_required
@user_type_required('Student')
def fees_parent(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    toady_date=datetime.now().date()
    records=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)

    fees_records=FeesAssign.objects.filter(student_id=request.student.id,branch_id=branch_id)
    # fees_discount=FeesTypeDiscount.objects.filter(branch=branch_id)
    fees_discount=DiscountAssign.objects.filter(student=request.student.id,branch_id=branch_id)
    paid_record=StudentFess.objects.filter(student=request.student.id,branch_id=branch_id)

    context={
        'records':records,'fees_records':fees_records,'toady_date':toady_date,'fees_discount':fees_discount,
        'paid_record':paid_record,'fees_parent':'active'
    }
    return render(request,'Student_part/fees_parent.html',context)

@login_required
@user_type_required('Student')
def hostel_room(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    records=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    context={
       'hostel_room':'active','record':records
            }
    return render(request,'Student_part/hostel_room.html',context)

@login_required
@user_type_required('Student')
def transport_routes(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    records=AssignVehicle.objects.filter(branch=branch_id)
    record=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    assign_vehicle=AssignVehicle.objects.filter(id=record.vehicle_number.id) if record.vehicle_number else None
    print("assign_vehicle===",assign_vehicle)
    context={
       'records':records,'transport_routes':'active','record':record,"assign_vehicle":assign_vehicle
            }
    return render(request,'Student_part/transport_routes.html',context)

@login_required
@user_type_required('Student')
def books(request):
    print("books-----",request.Session.id)
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    recordss =AddBook.objects.filter(branch=branch_id)
    print('===',recordss)
    record=LibrayMember.objects.filter(student=request.student.id,branch_id=branch_id).last()
    print('---',record)
    records=IssueBook.objects.filter(member=record,branch_id=branch_id)
    context={
        'records':records,'books':'active','record':record
            }
    return render(request,'Student_part/books.html',context)


@login_required
@user_type_required('Student')
def books_issued(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    print("student@@@",request.student.pk)
    record=LibrayMember.objects.filter(student=request.student.id,branch_id=branch_id).last()
    print("record@@@",record)
    records=IssueBook.objects.filter(member=record,branch_id=branch_id)
    print("records@@@",records.values())
    context={
        'books_issued':'active','records':records
            }
    return render(request,'Student_part/books_issued.html',context)

@login_required
@user_type_required('Student')
def teacher_reviews(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    student_obj=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    rating=TeacherRating.objects.filter(student=student_obj,branch_id=branch_id)
    rating_staff=[data.staff.id for data in rating]
    assign_teacher=AssignClassTeacher.objects.filter(Class=student_obj.Class,section=student_obj.section,branch_id=branch_id).last()
    if assign_teacher:
        records=assign_teacher.class_teacher.all()
    else:
        records=[]
    if request.method=='POST':
        TeacherRating.objects.get_or_create(
            student=student_obj,
            Class=student_obj.Class,
            section=student_obj.section,
            assign_teacher=assign_teacher,
            staff_id=request.POST.get('teacher_id'),
            rating=request.POST.get('rating'),
            comment=request.POST.get('comment'),
            branch_id=branch_id
        )
        return redirect('teacher_reviews_student')
    context={
        'teacher_reviews':'active','records':records,'rating_staff':rating_staff,'rating':rating
    }
    return render(request,'Student_part/teacher_reviews.html',context)

@login_required
@user_type_required('Student')
def notice_board(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    record=noticeBoard.objects.filter(branch=branch_id)
    context={
        'notice_board':'active','record':record
            }
    return render(request,'Student_part/notice_board.html',context)

@login_required
@user_type_required('Student')
def notice_board_view(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    records=noticeBoard.objects.filter(branch=branch_id)
    context={
        'records':records,'notice_board_view':'active'
            }
    return render(request,'Student_part/notice_board_view.html',context)

@login_required
@user_type_required('Student')
def attendance(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    records=StudentAttendance.objects.filter(branch=branch_id)
    record=StudentAttendance.objects.filter(student=request.student,branch_id=branch_id)
    print("record===",record)
    context={
        'records':records,'attendance':'active','record':record
            }
    return render(request,'Student_part/attendance.html',context)

@login_required
@user_type_required('Student')
def apply_leave(request):
    branch_name = request.session.get('branch_id', None)
    print("request.Session@@@", request.Session)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
   
   
    class_records=Class.objects.filter(branch=branch_id)
    section_records=Section.objects.filter(branch=branch_id)
    records=Addleave.objects.filter(student=request.student.id,branch_id=branch_id)
    student=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    form=AddleaveParentForm(initial={'Class':student.Class,'section':student.section,'student':student.id,})
    if request.method=='POST':
        form=AddleaveParentForm(request.POST)
        if form.is_valid():
            obj=form.save()            
            obj.branch_id = branch_id   
            obj.session = request.Session
            obj.save()
            return HttpResponseRedirect('/student/apply_leave')
        else:
            print(form.errors)
    context={
        'form':form,'records':records,'apply_leave':'active','class_records':class_records,'section_records':section_records
            }
    return render(request,'Student_part/apply_leave.html',context)

@login_required
@user_type_required('Student')
def apply_leave_edit(request,pk):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    records=Addleave.objects.filter(student=request.student.id,branch_id=branch_id)
    record=Addleave.objects.get(id=pk)
    form=AddleaveParentForm(instance=record)
    if request.method=='POST':
        form=AddleaveParentForm(request.POST,instance=record)
        if form.is_valid():
            obj=form.save()   
            obj.branch_id = branch_id
            obj.save()
            return HttpResponseRedirect('/student/apply_leave')
    context={
        'form':form,'records':records,'apply_leave':'active'
            }
    return render(request,'Student_part/apply_leave_edit.html',context)

@login_required
@user_type_required('Student')
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
    return HttpResponseRedirect('/student/apply_leave')



@login_required
@user_type_required('Student')
def homework(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=AssingHomeWork.objects.filter(student=request.student.id,branch_id=branch_id)
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
    return render(request,'Student_part/homework.html',context)


@login_required
@user_type_required('Student')
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
    return render(request,'Student_part/homework_view.html',context)

# Download center

@login_required
@user_type_required('Student')
def assignment_list(request):
    print("assignment_list-----",request.Session.id)
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='assignments',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
        'assignment_list':'active','records':records
    }
    return render(request,'Student_part/assignment_list.html',context)

@login_required
@user_type_required('Student')
def study_material(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='study_material',branch_id=branch_id)
    print("records===",records1)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    print("records===",records2)
    context={
         'study_material':'active','records':records,
    }
    return render(request,'Student_part/study_material.html',context)


@login_required
@user_type_required('Student')
def syllabus(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='syllabus',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
         'syllabus':'active','records':records,
    }
    return render(request,'Student_part/syllabus.html',context)


@login_required
@user_type_required('Student')
def other_download_list(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student = StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    records1=UploadContent.objects.filter(Class_id=student.Class,section_id=student.section,content_type='other_download',branch_id=branch_id)
    records2=UploadContent.objects.filter(Class_id__isnull=True,branch_id=branch_id)
    records=records1 | records2
    context={
         'other_download_list':'active','records':records,
    }
    return render(request,'Student_part/other_download_list.html',context)


@login_required
@user_type_required('Student')
def exam_schedule(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=ExamStudent.objects.filter(student=request.student.id,branch_id=branch_id,student__session=request.Session)
    context={
        'records':records,'exam_schedule':'active'
            }
    return render(request,'Student_part/exam_schedule.html',context)

@login_required
@user_type_required('Student')
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
    return render(request,'Student_part/exams_view.html',context)

@login_required
@user_type_required('Student')
def exam_result(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    records=ExamStudent.objects.filter(student=request.student.id,branch_id=branch_id)
    context={
        'records':records,'exam_result':'active'
            }
    return render(request,'Student_part/exam_result.html',context)


@login_required
@user_type_required('Student')
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
    return render(request,'Student_part/exam_result_view.html',context)


@login_required
@user_type_required('Student')
def class_timetable(request):
    print("assignment_list-----",request.Session)
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    TimeTable_records=TimeTable.objects.filter(Class=student.Class,section=student.section,session=request.Session,branch_id=branch_id)

    context={
        'TimeTable_records':TimeTable_records,'class_tim etable':'active'
            }
    return render(request,'Student_part/class_timetable.html',context)


@login_required
@user_type_required('Student')
def lesson_plan(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
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
            'lesson_plan_student':'active','Monday':Monday,'Tuesday':Tuesday,'Wednesday':Wednesday,'Thursday':Thursday,'Friday':Friday,'Saturday':Saturday,'Sunday':Sunday,
            'dates_in_week':dates_in_week,'week':week
                }
        return render(request,'Student_part/lesson_plan.html',context)
    context={
        'lesson_plan_student':'active'
            }
    return render(request,'Student_part/lesson_plan.html',context)


@login_required
@user_type_required('Student')
def syllabus_status(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)
    student=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    classs=student.Class
    section=student.section
    subject=SubjectGroup.objects.filter(Class=student.Class,section=student.section,branch_id=branch_id).last()
    print("subject",subject)
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
    context={
        'syllabus_status_student':'active','records':records,'chart_percent':chart_percent
    }
    return render(request, 'Student_part/syllabus_status.html', context)


@login_required
@user_type_required('Student')
def online_class(request):
    print("assignment_list-----",request.Session.id)
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
    print("branch_name@@@",branch_name)
    records = OnlineClass.objects.filter(branch=branch_id)
    if request.method == 'POST':
        form = OnlineClassForm(request.POST)
        if form.is_valid():
            form.save()
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.branch_id = branch_id
            obj.save()
            return redirect('/online_class')  # Redirect to a view showing the list of all online classes
    else:
        form = OnlineClassForm()

    context = {
        'records': records,
        'form': form,
        'online_class':'active'
    }

    return render(request, 'Student_part/online_class.html', context)

@login_required
@user_type_required('Student')
def online_class_feedback(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        records=Studentmeetingnote.objects.filter(branch=branch_id)
        form=StudentmeetingnoteForm ()
        record=OnlineClass.objects.get(id=pk)
        data_branch_id = record.branch.id
        if request.method=='POST':
            form=StudentmeetingnoteForm(request.POST)
            if form.is_valid():
                if branch_id == data_branch_id:
                    form.save()
                else:
                    form.instance.branch_id = branch_id
                form.save()
                return HttpResponseRedirect('/student/online_class')

        context={
            'form':form,'records':records,'online_class':'active','record':record,
                }
        return render(request,'Student_part/online_class_feedback.html',context)

@login_required
@user_type_required('Student')
def student_meeting_view(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
            print("branch_name@@@",branch_name)
        current_date = datetime.now()
        print('current_month',current_date)
        records=Studentmeetingnote.objects.filter(branch=branch_id)
        form=StudentmeetingnoteForm ()
        record=OnlineClass.objects.get(id=pk)
        meeting_url= request.POST.get('meeting_url')
        print('meeting_url',meeting_url)
        if request.method=='POST':
            student_attendance = OnlineClassAttendance.objects.filter(
                student=request.student.id,
                online=meeting_url,branch_id=branch_id
            )
            print('student_attendance',student_attendance)

            if not student_attendance.exists():
                OnlineClassAttendance.objects.get_or_create(
                    student_id=request.student.id,
                    online_id=meeting_url,
                    attendance_status='present',
                    attendance_date=current_date, 
                    branch_id=branch_id           
                )
        context={
            'form':form,'records':records,'staff_meeting':'active','record':record,
                }
        return render(request,'Student_part/student_meeting_view.html',context)


@login_required
@user_type_required('Student')
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
    return render(request,'Chat/chat_index_student.html',context)

@login_required
@user_type_required('Student')
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
            usertype='Student',
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
            usertype='Student',
            branch_id=branch_id
        )
    return redirect('chat_index')

@login_required
@user_type_required('Student')
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
    contact_obj= AddContact.objects.get(id=pk)
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
    return render(request,'Chat/chat_student.html',context)

@login_required
@user_type_required('Student')
def student_profile_update(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None  
        print("branch_name@@@",branch_name)

    records=StudentAdmission.objects.filter(branch=branch_id)
    record=Studentprofileupdate.objects.filter(branch=branch_id).first()
    if record:
        if record and record.fieldshide:
            student_fields_hide=record.fieldshide
        else:
            student_fields_hide=[]
    if records:
        record=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
        form=StudentsHideFieldForm(instance=record)
        if request.method=='POST':
            first_name=request.POST.get('first_name')
            if first_name:
                record.first_name=first_name
            last_name=request.POST.get('last_name')
            if last_name:
                record.last_name=last_name
            date_of_birth=request.POST.get('date_of_birth')
            if date_of_birth:
                record.date_of_birth=date_of_birth
            gender=request.POST.get('gender')
            if gender:
                record.gender_id=gender
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            Caste=request.POST.get('Caste')
            if Caste:
                record.Caste=Caste
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            mobile_number=request.POST.get('mobile_number')
            if mobile_number:
                record.mobile_number=mobile_number
            email=request.POST.get('email')
            if email:
                record.email=email
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            admission_date=request.POST.get('admission_date')
            if admission_date:
                record.admission_date=admission_date
            student_photo=request.POST.get('student_photo')
            if student_photo:
                record.student_photo=student_photo
            Blood_group=request.POST.get('Blood_group')
            if Blood_group:
                record.Blood_group=Blood_group
            height=request.POST.get('height')
            if height:
                record.height=height
            student_house=request.POST.get('student_house')
            if student_house:
                record.student_house_id=student_house
            weight=request.POST.get('weight')
            if weight:
                record.weight=weight
            category=request.POST.get('category')
            if category:
                record.category_id=category
            Father_name=request.POST.get('Father_name')
            if Father_name:
                record.Father_name=Father_name
            Father_phone=request.POST.get('Father_phone')
            if Father_phone:
                record.Father_phone=Father_phone
            Father_occupation=request.POST.get('Father_occupation')
            if Father_occupation:
                record.Father_occupation=Father_occupation
            Father_photo=request.POST.get('Father_photo')
            if Father_photo:
                record.Father_photo=Father_photo
            mother_name=request.POST.get('mother_name')
            if mother_name:
                record.mother_name=mother_name
            mother_photo=request.POST.get('mother_photo')
            if mother_photo:
                record.mother_photo=mother_photo
            mother_occupation=request.POST.get('mother_occupation')
            if mother_occupation:
                record.mother_occupation=mother_occupation
            if_guardian_is=request.POST.get('if_guardian_is')
            if if_guardian_is:
                record.if_guardian_is_id=if_guardian_is
            guardian_name=request.POST.get('guardian_name')
            if guardian_name:
                record.guardian_name=guardian_name
            guardian_relation=request.POST.get('guardian_relation')
            if guardian_relation:
                record.guardian_relation=guardian_relation
            guardian_email=request.POST.get('guardian_email')
            if guardian_email:
                record.guardian_email=guardian_email
            guardian_phone=request.POST.get('guardian_phone')
            if guardian_phone:
                record.guardian_phone=guardian_phone
            guardian_occupation=request.POST.get('guardian_occupation')
            if guardian_occupation:
                record.guardian_occupation=guardian_occupation
            guardian_photo=request.POST.get('guardian_photo')
            if guardian_photo:
                record.guardian_photo=guardian_photo
            guardian_address=request.POST.get('guardian_address')
            if guardian_address:
                record.guardian_address=guardian_address
            religion=request.POST.get('religion')
            if religion:
                record.religion=religion
            current_address=request.POST.get('current_address')
            if current_address:
                record.current_address=current_address
            permanent_address=request.POST.get('permanent_address')
            if permanent_address:
                record.permanent_address=permanent_address
            bank_account_number=request.POST.get('bank_account_number')
            if bank_account_number:
                record.bank_account_number=bank_account_number
            bank_name=request.POST.get('bank_name')
            if bank_name:
                record.bank_name=bank_name            
            if branch_id:
                record.branch_id=branch_id    
            ifsc_code=request.POST.get('ifsc_code')            
            if ifsc_code:
                record.ifsc_code=ifsc_code
            national_identification_number=request.POST.get('national_identification_number')
            if national_identification_number:
                record.national_identification_number=national_identification_number
            local_identification_number=request.POST.get('local_identification_number')
            if local_identification_number:
                record.local_identification_number=local_identification_number
            rte=request.POST.get('rte')
            if rte:
                record.rte_id=rte
            previous_school_detail=request.POST.get('previous_school_detail')
            if previous_school_detail:
                record.previous_school_detail=previous_school_detail
            record.save()
            form=StudentsHideFieldForm(request.POST,request.FILES,instance=record)
            if form.is_valid():
                obj=form.save()
                obj.branch_id = branch_id
                obj.save()  
                return HttpResponseRedirect('/student/student_profile_update')
            else:
                print(form.errors)

    context={
             'records':records,'form':form,'student_fields_hide':student_fields_hide,'record':record
            }
    return render(request,'Student_part/student_profile_update.html',context)


@login_required
@user_type_required('Student')
def hostel_room(request):
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None
    print("branch_name@@@",branch_name)
    records=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    hostel_records=HostelRoom.objects.filter(id=records.route_list.id ,branch_id=branch_id) if records.route_list else []
    context={
       'hostel_room':'active','record':records,"hostel_records":hostel_records
            }
    return render(request,'Student_part/hostel_room.html',context)



    
  

@login_required
@user_type_required('Student')
def online_exam(request):
    
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    current_date = date.today()
    student_admission_record=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    
    print("request.user.id ===", student_admission_record.Class,student_admission_record.section)

    # Fetch all EnrollmentAssign records related to the student's class
    enrollment_assign_records = EnrollmentAssign.objects.filter(Class=student_admission_record.Class,section=student_admission_record.section)
    

    # Loop through each EnrollmentAssign record
    # question_paper_ids = []
    # for enrollment_assign in enrollment_assign_records:
    #     print("enrollment_assign===", enrollment_assign.enrollment)

    #     # Fetch the corresponding Enrollment record
    #     enrollment_record = Enrollment.objects.get(id=enrollment_assign.enrollment.id)
    #     print("Question paperID===", enrollment_record.question_paper.id)
    #     question_paper_id = enrollment_record.question_paper.id
    #     question_paper_ids.append(question_paper_id)
    # print("question_paper_ids===", question_paper_ids)    
    # question_paper=QuestionPaper.objects.filter(id__in=question_paper_ids)
    # print("question_paper===", question_paper)

    #     # Fetch all Question records related to the question paper
      
    # question_records = Question.objects.filter(question_paper__in=question_paper_ids)
    
    # print("Questionrecords===", question_records)
        
    
    context={
        'online_exam':'active',"question_records":enrollment_assign_records,"current_date":current_date
    }
    return render(request,'Student_part/online_exam.html',context) 

def online_papers(request):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None    
        records = QuestionPaper.objects.filter(branch=branch_id) 
        print("questions++",records)
        # l=[]
        # print('questions',questions)
        # for data in questions:
        #     eval(data.options)
        #     l.append(data)
        #     print("data******",type(data.options))
                 
           
        context = {
                   "records":records,
                   "school_registration": "active"}
        return render(request, "Student_part/online_paper.html", context)
    # except Exception as error:
    #     return render(request, "error.html", {"error": error}) 

   
from datetime import timedelta
   
def question_models(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
        

        enrollment_assign = EnrollmentAssign.objects.get(id=pk, branch_id=branch_id)
        print("111enrollment_assign++", enrollment_assign)
        enrollment_record = Enrollment.objects.get(id=enrollment_assign.enrollment.id)
        print("Enrollment_record====", enrollment_record.allowed_time)

        # Retrieve the values
        # Assuming allowed_time is an integer representing the number of minutes
       
        question_paper_record = QuestionPaper.objects.get(id=enrollment_record.question_paper.id)
        print("question_paper----",question_paper_record.duration)
        questionss = Question.objects.filter(question_paper=question_paper_record,branch_id=branch_id)
        print("questionss===----",questionss)
        # Enrollment_record.start_time = 
        
        
        # print("questions++",questionss)
        # question_paper = QuestionPaper.objects.get(id=pk)        
        # print("question_paper++",question_paper)
        # enrollment_record = Enrollment.objects.filter(question_paper=question_paper)       
        # print("enrollment_record++",enrollment_record)
        student_admission_record=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
        print("student_admission_record++",student_admission_record)
        if request.method == 'POST':
            # questions = request.POST.getlist('questions')
            # print("questions----", questions)                 
                # Retrieve the selected option for each question
            # selected_option = request.POST.get(f"answers_{question_id.id}")
            # print("answers_===", selected_option)
                
            student_answers_records=StudentAnswers.objects.create(
                student=student_admission_record,
                question_paper=question_paper_record,
                branch_id=branch_id
                ) 
            
            for question_id in questionss:
                # Get the option from the request.POST dictionary for each question
                selected_option = request.POST.get(f"answers_{question_id.id}")

                print("selected_option",type(selected_option))    
                # Create the AnswerPeperSubmit record for each question
                AnswerPeperSubmit.objects.create(
                    student_answers=student_answers_records,                   
                    questiones=question_id,  # Assuming 'questiones' refers to the question instance
                    options=selected_option,  # Save the selected option directly
                    mark=question_id.mark,
                    branch_id=branch_id
                )

            return HttpResponseRedirect('/student/online_exam') 
       
        
        context = {
            "questions": questionss,
            "Enrollment_record": enrollment_record,
            "school_registration": "active",
            "question_paper_record":question_paper_record
        }
        return render(request, "Student_part/online_exam_assign.html",context)      
        
        
                

       

    # except Exception as error:
    #     return render(request, "error.html", {"error": error})      

def time_check(request,pk):
        branch_name = request.session.get('branch_id', None)
        if branch_name:
            branch_id = branch_name       
        else:
            branch_id = None  
        print("branch_name@@@",branch_name) 
        current_time = datetime.now()
        formatted_time = current_time.strftime("%H:%M:%S")
        # Convert formatted_time to a datetime.time object
        current_time_obj = datetime.strptime(formatted_time, "%H:%M:%S").time()
        print("current_time_obj---", current_time_obj)
        enrollment_assign = EnrollmentAssign.objects.get(id=pk, branch_id=branch_id)
        print("enrollment_assign++", enrollment_assign.enrollment)
        enrollment_record = Enrollment.objects.get(id=enrollment_assign.enrollment.id)
        print("Enrollment_record====", enrollment_record.allowed_time)
        start_time = enrollment_record.start_time

        # Convert start_time to a datetime object, assuming today's date for the conversion
        start_time_as_datetime = datetime.combine(datetime.today(), start_time)

        # Convert allowed_time to an integer and create a timedelta
        extra_time = timedelta(minutes=int(enrollment_record.allowed_time))

        # Adding extra time to start_time
        new_time_as_datetime = start_time_as_datetime + extra_time

        # Extracting just the time portion
        new_time = new_time_as_datetime.time()
        print("===time",new_time)
        if start_time <= current_time_obj <= new_time:
            print("ifpass") 
            return redirect(f"/student/question_models/{pk}") 
        elif enrollment_record.any_time == True :
            return redirect(f"/student/question_models/{pk}")            
        else:
            return render(request, "Student_part/online_exam_retrun.html")      

def online_exam_complete(request):             
           
        context = {
                  
                   "school_registration": "active"}
        return render(request, "Student_part/online_exam_complete.html", context)
    # except Exception as error:
    #     return render(request, "error.html", {"error": error})         
    
@login_required
@user_type_required('Student')
def online_exam_result(request):
    
    branch_name = request.session.get('branch_id', None)
    if branch_name:
        branch_id = branch_name       
    else:
        branch_id = None    
    print("branch_name@@@",branch_name)
    current_date = date.today()
    student_admission_record=StudentAdmission.objects.get(id=request.student.id,branch_id=branch_id)
    
    print("request.user.id ===", student_admission_record.Class,student_admission_record.section)
    stuednt_result=PaperCorrection.objects.filter(student=student_admission_record)
    exam_date=[]
    for data in  stuednt_result: 
        question=data.question_paper
        stuednt_results=Enrollment.objects.get(question_paper=question)
        print("stuednt_results",stuednt_results.exam_date) 
        exam_date.append(stuednt_results.exam_date)
    print("exam_date",exam_date)     

    
    context={
        'online_exam_result':'active',"record":stuednt_result
    }
    return render(request,'Student_part/online_exam_result.html',context)     