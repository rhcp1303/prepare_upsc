from django.contrib import admin
from django.urls import path
import questions.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_mock_mcq/', views.get_mock_mcq, name='get_mock_mcq'),
    path('api/mock_test_view/', views.mock_test_view, name='mock_test_view'),
    path('api/demo_view/', views.demo_view, name='demo_view'),
    path('api/demo2_view/', views.demo2_view, name='demo2_view'),

]
