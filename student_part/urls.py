from django.urls import path,include
from student_part import views
urlpatterns=[
    path('',views.signup,name='signup'),
    path('student_dashboard', views.student_dashboard,name='student_dashboard_student'),
    path('fees', views.fees_parent,name='fees_student'),
    path('hostel_room', views.hostel_room,name='hostel_room_student'),
    path('transport_routes', views.transport_routes,name='transport_routes_student'),
    path('books', views.books,name='books_student'),
    path('books_issued', views.books_issued,name='books_issued_student'),
    path('teacher_reviews', views.teacher_reviews,name='teacher_reviews_student'),
    path('notice_board', views.notice_board,name='notice_board_student'),
    path('apply_leave', views.apply_leave,name='apply_leave_student'),
    path('apply_leave_edit/<pk>', views.apply_leave_edit,name='apply_leave_edit_student'),
    path('apply_leave_delete/<pk>', views.apply_leave_delete,name='apply_leave_delete_student'),
    path('online_exam', views.online_exam,name='online_exam_student'),
    path('homework', views.homework,name='homework_student'),
    path('homework_view/<pk>', views.homework_view,name='homework_view'),
# Download sneter
    path('assignment_list', views.assignment_list,name='assignment_list_student'),
    path('study_material', views.study_material,name='study_material_student'),
    path('syllabus', views.syllabus,name='syllabus_student'),
    path('other_download_list', views.other_download_list,name='other_download_list_student'),
    path('attendance', views.attendance,name='attendance_student'),
    path('exam_schedule', views.exam_schedule,name='exam_schedule_student'),
    path('exams_view/<pk>', views.exams_view,name='exams_view_student'),
    path('exam_result', views.exam_result,name='exam_result_student'),
    path('notice_board_view', views.notice_board_view,name='notice_board_view_student'),
    path('class_timetable', views.class_timetable,name='class_timetable_student'),
    path('exam_result_view/<pk>', views.exam_result_view,name='exam_result_view_student'),
    path('lesson_plan', views.lesson_plan,name='lesson_plan_student'),
    path('syllabus_status', views.syllabus_status,name='syllabus_status_student'),
    path('online_class', views.online_class,name='online_class_student'),
    path('online_class_feedback/<pk>', views.online_class_feedback,name='online_class_feedback_student'),
    path('student_meeting_view/<pk>', views.student_meeting_view,name='student_meeting_view_student'),

    path('chat_index', views.chat_index, name='chat_index_student'),
    path('save_contact', views.save_contact, name='save_contact_student'),
    path('chat/<pk>', views.chat, name='chat_student'),
    path('student_profile_update', views.student_profile_update,name='student_profile_update_student'),

    path("question_models/<pk>",views.question_models,name="student_question_models"),
    path('online_papers', views.online_papers,name='student_online_papers'),
    path('time_check/<pk>', views.time_check,name='time_check'),
    path('online_exam_complete', views.online_exam_complete, name='student_online_exam_complete'),    
    path('online_exam_result', views.online_exam_result, name='student_online_exam_result')


]
