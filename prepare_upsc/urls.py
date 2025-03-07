from django.contrib import admin
from django.urls import path
import questions.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_subject_wise_mock_mcq/', views.get_subject_wise_mock_mcq, name='get_mock_mcq'),
    path('api/get_year_wise_pyq/', views.get_year_wise_pyq, name='get_year_wise_pyq'),
    path('api/get_comprehensive_mock_mcq/', views.get_comprehensive_mock_mcq, name='get_comprehensive_mock_mcq'),
    path('api/subject_wise_mock_test/', views.subject_wise_mock_test_view, name='subject_wise_mock_test_view'),
    path('api/quiz/', views.quiz_view, name='quiz_view'),
    path('api/pyq/', views.pyq_view, name='pyq_view'),
    path('api/get_quiz_questions/', views.get_quiz_questions, name='get_quiz_questions'),
]
