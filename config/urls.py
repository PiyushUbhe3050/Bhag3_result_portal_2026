from django.contrib import admin
from django.urls import path
from results import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.search_result, name='search_result'),
    path('analytics/', views.admin_analytics, name='admin_analytics'),
]
