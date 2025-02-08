from django.contrib import admin
from django.urls import path
import questions.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('generate_mock_test/', views.generate_mock_test, name='generate_mock_test'),

]
