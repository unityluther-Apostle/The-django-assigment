from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    # Student URLs
    path('', views.feed_view, name='feed'),
    path('announcement/<int:pk>/', views.announcement_detail, name='announcement_detail'),

    # Admin URLs
    path('manage/', views.AdminDashboardView.as_view(), name='manage_dashboard'),
    path('manage/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('manage/<int:pk>/edit/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('manage/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
]
