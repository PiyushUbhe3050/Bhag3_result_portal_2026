from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_result, name='search_result'),
    path('result/<int:student_id>/', views.view_report_card, name='view_report_card'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
]