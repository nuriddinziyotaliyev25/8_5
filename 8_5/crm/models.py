from django.db import models
from django.contrib.auth.models import AbstractUser

ADMIN, MODERATOR, TEACHER, STUDENT = ('admin', 'moderator', 'teacher', 'student')


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Yangilangan sana")

    class Meta:
        abstract = True


class User(AbstractUser, Base):
    ROLE_CHOICES = (
        (ADMIN, "Administrator"),
        (MODERATOR, "Moderator"),
        (TEACHER, "O'qituvchi"),
        (STUDENT, "O'quvchi")
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default=STUDENT, verbose_name="Rol")
    image = models.ImageField(upload_to='user/', null=True, blank=True, verbose_name="Rasm")

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"

    def __str__(self):
        return self.get_full_name()

    def get_image(self):
        if self.image:
            return self.image.url
        return "https://jeffjbutler.com//wp-content/uploads/2018/01/default-user.png"


class Course(Base):
    title = models.CharField(max_length=100, verbose_name="Kurs nomi")
    description = models.TextField(null=True, blank=True, verbose_name="Kurs tavsifi")
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="O'qituvchi")

    class Meta:
        verbose_name = "Kurs"
        verbose_name_plural = "Kurslar"

    def __str__(self):
        return self.title


class Enrollment(Base):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Foydalanuvchi")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")

    class Meta:
        verbose_name = "Ro'yxatdan o'tish"
        verbose_name_plural = "Ro'yxatdan o'tishlar"

    def __str__(self):
        return self.user.get_full_name() + ' - ' + self.course.title


class Lesson(Base):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Kurs")
    title = models.CharField(max_length=255, verbose_name="Dars nomi")
    content = models.FileField(upload_to='lesson/', null=True, blank=True, verbose_name="Qo'shimcha fayl")

    class Meta:
        verbose_name = "Dars"
        verbose_name_plural = "Darslar"

    def __str__(self):
        return self.course.title + ' - ' + self.title


class Assignment(Base):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name="Dars")
    title = models.CharField(max_length=255, verbose_name="Vazifa nomi")
    description = models.TextField(null=True, blank=True, verbose_name="Vazifa tavsifi")
    content = models.FileField(upload_to='assignment/', null=True, blank=True, verbose_name="Qo'shimcha fayl")
    due_date = models.DateTimeField(verbose_name="Topshirish muddati")

    class Meta:
        verbose_name = "Vazifa"
        verbose_name_plural = "Vazifalar"

    def __str__(self):
        return self.lesson.title + ' - ' + self.title
