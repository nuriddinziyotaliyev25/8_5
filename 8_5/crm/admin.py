from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import User, Course, Enrollment, Lesson, Assignment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'created_at', 'updated_at', 'show_image')
    list_filter = ('role', 'created_at')
    search_fields = ('username', 'email')

    def show_image(self, obj: User):
        return mark_safe(f'<img src="{obj.get_image()}" alt="No image" style="width: 70px; height: 70px; border-radius: 50%;">')
    show_image.short_description = "Rasm"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'created_at', 'updated_at')
    list_filter = ('teacher', 'created_at')
    search_fields = ('title', 'description')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('course', 'created_at')
    search_fields = ('user__username', 'course__title')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at', 'updated_at')
    list_filter = ('course', 'created_at')
    search_fields = ('title', 'course__title')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'due_date', 'created_at', 'updated_at')
    list_filter = ('lesson', 'due_date', 'created_at')
    search_fields = ('title', 'lesson__title')
