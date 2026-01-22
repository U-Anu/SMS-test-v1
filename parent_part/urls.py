from django.urls import path
from parent_part import views
urlpatterns=[
    path('parent_dashboard', views.parent_dashboard,name='parent_dashboard'),
    path('fees_parent', views.fees_parent,name='fees_parent'),
    path('hostel_room', views.hostel_room,name='hostel_room_parent'),
    path('transport_routes', views.transport_routes,name='transport_routes'),
    path('books', views.books,name='books'),
    path('books_issued', views.books_issued,name='books_issued'),
    path('teacher_reviews', views.teacher_reviews,name='parent_teacher_reviews'),
    path('notice_board_parent', views.notice_board,name='notice_board_parent'),
    path('apply_leave_parent', views.apply_leave,name='apply_leave_parent'),
    path('apply_leave_edit/<pk>', views.apply_leave_edit,name='apply_leave_edit'),
    path('apply_leave_delete/<pk>', views.apply_leave_delete,name='apply_leave_delete'),
    path('online_exam', views.online_exam,name='online_exam'),
    path('parent_homework', views.homework,name='parent_homework'),
    path('parent_homework_view/<pk>', views.homework_view,name='parent_homework_view'),
# Download sneter
    path('assignment_list', views.assignment_list,name='assignment_list_parent'),
    path('study_material', views.study_material,name='study_material_parent'),
    path('syllabus', views.syllabus,name='syllabus_parent'),
    path('other_download_list', views.other_download_list,name='other_download_list_parent'),
    # path('attendance_parent', views.attendance,name='attendance_parent'),
    path('exam_schedule_parent', views.exam_schedule,name='exam_schedule_parent'),
    path('exams_view/<pk>', views.exams_view,name='exams_view'),
    path('exam_result', views.exam_result,name='parent_exam_result'),
    path('notice_board_view', views.notice_board_view,name='notice_board_view'),
    path('class_timetable', views.class_timetable,name='parent_class_timetable'),
    path('exam_result_view/<pk>', views.exam_result_view,name='parent_exam_result_view'),
    path('attendance_parent', views.attendance,name='attendance_parent'),
    path('lesson_plan', views.lesson_plan,name='lesson_plan_parent'),
    path('syllabus_status', views.syllabus_status,name='syllabus_status_parent'),
    path('parent_meeting', views.parent_meeting,name='parent_meeting_parent'),
    path('parent_meeting_feeedback/<pk>', views.parent_meeting_feeedback,name='parent_meeting_feeedback_parent'),
    path('parent_meeting_view/<pk>', views.parent_meeting_view,name='parent_meeting_view_parent'),

    path('chat_index', views.chat_index, name='chat_index_parent'),
    path('save_contact', views.save_contact, name='save_contact_parent'),
    path('chat/<pk>', views.chat, name='chat_parent'),


]