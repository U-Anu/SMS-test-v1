from django.urls import path,include
from API import views
urlpatterns=[
    path('student',views.student_get),
    path('staff',views.staff_get),
    path('student-detail/',views.StudentAdmissionApiView.as_view(),name='student_detail_api'),
    path('user-type/',views.UserTypeApiView.as_view(),name='user_type_api'),
    path('home-work/',views.HomeWorkView.as_view(),name='api_home_work_student'),
    path('student-attendance/',views.AttendanceView.as_view(),name='api_attendance'),
    path('add-homework/', views.AddHomeWorkListCreateView.as_view(), name='homework-list-create_api'),
    path('homework/<int:pk>/', views.AddHomeWorkDetailView.as_view(), name='homework-detail_api'),
    path('classes/', views.ClassListView.as_view(), name='class-list_api'),
    path('classes/sections/<int:class_id>/', views.SectionsByClassView.as_view(), name='class-sections_api'),
    path('subject-groups/<int:class_id>/<int:section_id>/', views.SubjectGroupByClassAndSectionView.as_view(), name='api_subject_groups'),
    path('subject/<int:sub_group_id>/', views.SubjectBySubjectGroupClassView.as_view(), name='api_subject'),
    path('student-leave/',views.StudentLeaveListCreateView.as_view(),name='api_student_leave'),
    path('student-list/<int:class_id>/<int:section_id>/',views.StudentByClassandSectionView.as_view(),name='api_student_list'),
    path('apply-leave/',views.AddleaveView.as_view(),name='apply-leave_api'),
    path('available-leave/',views.AvailableLeaveListCreateView.as_view(),name='available-leave_api'),
    path('staff-leave/',views.StaffLeaveListCreateView.as_view(),name='staff-leave_api'),
    path('add-routes/',views.RountCreateView.as_view(),name='add-routes_api'),
    path('add-vehicle/',views.Vehiclecreateview.as_view(),name='add-vehicle_api'),
    path('add-assignVehicle/',views.AssignVehiclecreateview.as_view(),name='add-assignVehicle_api'),
    path('route/',views.Rountlistcreateview.as_view(),name='route_api'),
    path('Vehicle/',views.Vehiclelistcreateview.as_view(),name='Vehicle_api'),
    path('Staff-role/',views.StaffRoleview.as_view(),name='Staff-role_api'),
    path('Staff-Attendance/',views.StaffAttendanview.as_view(),name='Staff-Attendance_api'),
    path('one-student-attendance/',views.StudenceAttendanview.as_view(),name='one-student-attendance_api'),
    path('student-approve-leave/<int:pk>/', views.StudenceAttendanlistview.as_view(), name='student-approve-leave_api'),
    path('add-hostel/',views.Hostelcreateview.as_view(),name='add-hostel_api'),
    path('room-type/',views.RoomTypecreateview.as_view(),name='room-type_api'),
    path('hostel-room/',views.HostelRoomcreateview.as_view(),name='hostel-room_api'),
    path('student-hostel/',views.StudentHostelview.as_view(),name='student-hostel_api'),
    path('routes/',views.Routeview.as_view(),name='routes_api'),
    path('Vehicle/',views.Vehicleview.as_view(),name='Vehicle_api'),
    path('Student-hostellist/',views.StudentAdmissionHostelview.as_view(),name='Student-hostellist_api'),
    path('Student-user/',views.StudentAdmissionuserview.as_view(),name='Student-user_api'),
    path('Staff-user/',views.StaffAttendanuserview.as_view(),name='Staff-user_api'),
    path('hostel/',views.Hostelview.as_view(),name='hostel_api'),
    path('roomtype/',views.RoomTypeview.as_view(),name='roomtype_api'),
    path('add-lesson/',views.Lessonview.as_view(),name='add-lesson_api'),
    path('subject-name/',views.Subjectsview.as_view(),name='subject-name_api'),
    path('lesson-name/',views.Lessonnameview.as_view(),name='lesson-name_api'),
    path('topic/',views.topicview.as_view(),name='topic_api'),
    path('student-lesson/',views.StudentLessonView.as_view(),name='student-lesson_api'),
    path('lesson-plan/',views.LessonPlanView.as_view(),name='lesson-plan_api'),
    path('topic-name/',views.topinamecview.as_view(),name='topic-name_api'),
    path('time-table/',views.timetablecview.as_view(),name='time-table_api'),
    path('assignment-list/',views.Assignmentsview.as_view(),name='assignment-list_api'),
    path('study-material/',views.studymaterialview.as_view(),name='study-material_api'),
    path('syllabus/',views.syllabusview.as_view(),name='syllabus_api'),
    path('other-download/',views.otherdownloadview.as_view(),name='other-download_api'),
    path('upload-content/',views.uploadcontentview.as_view(),name='upload-content_api'),
    path('staff-meeting/',views.StaffMeetingview.as_view(),name='staff-meeting_api'),
    path('Parent-meeting/',views.ParentMeetingview.as_view(),name='Parent-meeting_api'),
    path('online-class/',views.OnlineClassview.as_view(),name='online-class_api'),
    path('add-staff/',views.AddStaffview.as_view(),name='add-staff_api'),
    path('Student-meeting/',views.StudentAdmissionmeetingview.as_view(),name='Student-hostellist_api'),
    path('class/',views.Classview.as_view(),name='class_api'),
    path('section/',views.Sectionview.as_view(),name='section_api'),
    path('subjects/',views.Subjectsnameview.as_view(),name='subjects_api'),
    path('subject-group/',views.SubjectGroupnameview.as_view(),name='subject-group_api'),
    path('assign-class-teacher/',views.AssignClassTeacherview.as_view(),name='assign-class-teacher_api'),
    path('timetable/',views.TimeTableview.as_view(),name='timetable_api'),

    path('staff-name/',views.AddStaffnameview.as_view(),name='staff-name_api'),

    path('stu-mark-sheet/',views.DesignMarkSheetview.as_view(),name='stu-mark-sheet_api'),
    path('stu-admit-card/',views.AdmitCardview.as_view(),name='stu-admit-card_api'),
    path('stu-admit-card/<int:pk>/', views.AdmitCardNameview.as_view(), name='stu-admit-card_api'),
    path('exam-group/',views.AddExamview.as_view(),name='exam-group_api'),
    path('exam-result/',views.EntryMarksview.as_view(),name='exam-result_api'),

    path('promote-student/',views.PromoteStudentview.as_view(),name='promote-student_api'),
    path('promote-stu/<int:pk>/',views.PromoteStudentNameview.as_view(),name='promote-stu_api'),
    path('stu-timetbale/',views.TimeTableStudentview.as_view(),name='stu-timetbale_api'),
    path('staff-timetbale/',views.TimeTablestaffview.as_view(),name='staff-timetbale_api'),
    path('add-exam-sub/',views.AddExamSubjectview.as_view(),name='add-exam-sub_api'),
    path('print-admit-card/',views.printadmitview.as_view(),name='print-admit-card_api'),
    path('print-mark-sheet/',views.printmarkview.as_view(),name='print-mark-sheet_api'),

#  17 october

    path('fees-discount/',views.FeesTypeDiscountview.as_view(),name='fees-discount_api'),
    path('fees-type/',views.FeesTypeview.as_view(),name='fees-type_api'),
    path('fees-group/',views.FeesGroupview.as_view(),name='fees-group_api'),
    path('fees-master/',views.FeesMasterview.as_view(),name='fees-master_api'),

    path('search-due-fee/',views.FeesAssignview.as_view(),name='search-due-fee_api'),

    path('search-due-stu/',views.FeesTypeDiscountstuview.as_view(),name='search-due-stu_api'),

    path('fees-master-stu/',views.FeesMasterstuview.as_view(),name='fees-master-stu_api'),

    path('fees-type/',views.FeesTypestuview.as_view(),name='fees-type_api'),

    path('search-fee-payment/',views.StudentFessview.as_view(),name='search-fee-payment_api'),
    path('fees-dis/',views.DiscountAssignview.as_view(),name='fees-dis_api'),

# 18 october

    path('staff-leave-type/',views.AddLeaveTypenamesview.as_view(),name='staff-leave-type_api'),
    path('add-leave-type/',views.AddLeaveTypeNameview.as_view(),name='add-leave-type_api'),
    path('approve-leave/',views.ApproveLeaveNameview.as_view(),name='approve-leave_api'),
    path('staff-department/',views.Departmentview.as_view(),name='staff-department_api'),
    path('staff-disbale/',views.AddStaffdisview.as_view(),name='staff-disbale_api'),
    path('staff-designation/',views.Designationview.as_view(),name='staff-designation_api'),
    path('stu-leave/',views.Addleavestuview.as_view(),name='stu-leave_api'),

# 19 October
    path('Student-Profile/<int:pk>/',views.StudentAdmissionStudentView.as_view(), name='Student-Profile_api'),
    path('student-disbale/',views.StudentAdmissionstudisview.as_view(),name='student-disbale_api'),
    path('student-category/',views.StudentCategorystudisview.as_view(),name='student-category_api'),
    path('student-bulk-del/<int:pk>/',views.StudentAdmissionStudentbulkView.as_view(), name='student-bulk-del_api'),
    path('student-profile/',views.Studentprofilestudisview.as_view(),name='student-profile_api'),

# 20 October

   path('student-admission-add/',views.StudentAdmissionaddview.as_view(),name='student-admission-add_api'),
   path('student-house/',views.StudentHouseview.as_view(),name='student-house_api'),
   path('disable-reason/',views.DisableReasonview.as_view(),name='disable-reason_api'),

# 23 october

   path('exam-student/',views.ExamStudentview.as_view(),name='exam-student_api'),
   
   path('currency/create/',views.CurrencyCreateAPIView.as_view(), name='currency-create'),
]