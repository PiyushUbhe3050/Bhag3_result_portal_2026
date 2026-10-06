from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_result, name='search_result'),
    path('result/<int:student_id>/', views.view_report_card, name='view_report_card'),
    path('bulk-upload/', views.bulk_upload_students, name='bulk_upload'),
    path('download-sample-csv/', views.download_sample_csv, name='download_sample_csv'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
]