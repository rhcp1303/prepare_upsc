from django.contrib import admin
from django.urls import path
import questions.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_subjectwise_mock_mcq/', views.get_subjectwise_mock_mcq, name='get_mock_mcq'),
    path('api/get_yearwise_pyq/', views.get_yearwise_pyq, name='get_yearwise_pyq'),
    path('api/get_comprehensive_mock_mcq/', views.get_comprehensive_mock_mcq, name='get_comprehensive_mock_mcq'),
    path('api/mock_test_view/', views.mock_test_view, name='mock_test_view'),
    path('api/demo_view/', views.demo_view, name='demo_view'),
    path('api/demo2_view/', views.demo2_view, name='demo2_view'),
    path('api/demo3_view/', views.demo3_view, name='demo3_view'),
    path('api/demo4_view/', views.demo4_view, name='demo4_view'),
    path('api/get_quiz_questions/', views.get_quiz_questions, name='get_quiz_questions'),
]
