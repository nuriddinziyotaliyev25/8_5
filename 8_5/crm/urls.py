from django.urls import path

from . import views

app_name = 'crm'
urlpatterns = [
    path('user/list/', views.UserListView.as_view(), name="user-list"),
    path('user/<int:pk>/detail/', views.UserDetailView.as_view(), name="user-detail"),

    path('course/list/', views.CourseListView.as_view(), name="course-list"),
    path('course/<int:pk>/detail/', views.CourseDetailView.as_view(), name="course-detail"),

    path('enrollment/list/', views.EnrollmentListView.as_view(), name="enrollment-list"),
    path('enrollment/<int:pk>/detail/', views.EnrollmentDetailView.as_view(), name="enrollment-detail"),
]