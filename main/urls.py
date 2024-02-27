from django.urls import path
from .views import login, information_view, get_banner, filter_university, get_about, popular_university, popular_faculty, get_about_me, get_testimonials, \
    create_contact, university_details, student_cabinet, student_university, student_university_single, personal_manager, \
    university_admin_panel, university_students, university_registered_students, university_registered_student_single, \
    university_registered_student_answer, university_cabinet, dashboard, dashboard_university, dashboard_university_single, \
    dashboard_student, dashboard_student_single

urlpatterns = [
    path('login/', login),
    path('informayion/', information_view, name='information_view'),
    path('get-banner/', get_banner),
    path('filter-university/', filter_university),
    path('get-about/', get_about),
    path('popular-univeristy/', popular_university),
    path('popular-faculty/', popular_faculty),
    path('get-about-me/', get_about_me),
    path('get-testimonials/', get_testimonials),
    path('create-contact/', create_contact),
    path('university-details/<int:pk>/', university_details),
    path('student-cabinet/<int:pk>/', student_cabinet),
    path('student-university/<int:pk>/', student_university),
    path('student-university-single/<int:pk>/', student_university_single),
    path('personal-manager/<int:pk>/', personal_manager, name='personal-manager'),
    path('university-admin-panel/<int:pk>/', university_admin_panel),
    path('university-students/<int:pk>/', university_students),
    path('university-registered-student/<int:pk>/', university_registered_students),
    path('university-registered-student-single/<int:pk>/', university_registered_student_single),
    path('university-registered-student-answer/<int:pk>/', university_registered_student_answer),
    path('university-cabinet/<int:pk>/', university_cabinet),
    path('dashboard/', dashboard),
    path('dashboard-university/', dashboard_university),
    path('dashboard-university-single/<int:pk>/', dashboard_university_single),
    path('dashboard-students/', dashboard_student),
    path('dashboard-student-single/<int:pk>/', dashboard_student_single)
]