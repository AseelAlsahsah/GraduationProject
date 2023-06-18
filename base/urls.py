from django.urls import path
from . import views

urlpatterns = [
    # **************************************************** AUTHENTICATION **********************************
    path('', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('studentSignup/', views.student_signup, name="studentSignup"),
    path('consultantSignup/', views.consultant_signup, name="consultantSignup"),

    # **************************************************** STUDENT *****************************************
    path('home/', views.home, name="home"),
    path('disorders/disordersContent/<int:pk>/', views.disorder_detail, name="disordersContent"),
    path('dailyRoutines/', views.daily_routines, name="dailyRoutines"),
    path('ourTeam/', views.ourTeam, name="ourTeam"),
    path('FAQ/', views.FAQ, name="FAQ"),

    path('bookAppointment/suitableConsultants/<str:symptom>/', views.suitable_consultants, name="consulPage"),
    path('bookAppointment/availableTimes/<int:pk>/<str:symptom>/', views.available_times, name="availableTimes"),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('bookAppointment/Test/<int:pk>/', views.test_view, name="test"),

    path('studentHistory/<str:pk>/', views.student_history, name="studentHistory"),
    path('std_scaledFeedback/', views.student_scaledFeedback, name="std_scaledFeedback"),
    path('studentSessions/<str:pk>/', views.student_sessions, name="studentSessions"),
    path('delete-session/', views.delete_session, name='delete_session'),


    # **************************************************** CONSULTANT **************************************
    path('consultant/consultantDashboard/<str:pk>/', views.consultant_dashboard, name="consultantDashboard"),
    path('consultant/editConsultantInfo/<str:pk>/', views.edit_consultant_info, name="editConsultant"),

    # **************************************************** CHAT SESSION **************************************
    path('chat/stdChatSession/<int:session_pk>/', views.student_chat, name="student_chat"),
    path('chat/consChatSession/<int:session_pk>/', views.consultant_chat, name="consultant_chat"),
    path('consultant/give_scaledFeedback/<int:pk>/', views.give_scaledFeedback, name="give_scaledFeedback"),

    path('std_enter_session/', views.std_enter_session, name='std_enter_session'),
    path('consul_enter_session/', views.consul_enter_session, name='consul_enter_session'),

]
