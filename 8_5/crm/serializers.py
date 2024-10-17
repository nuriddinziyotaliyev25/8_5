from rest_framework import serializers
from .models import User, Course, Enrollment

class UserSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    password2 = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False)
    new_password2 = serializers.CharField(write_only=True, required=False, label="Yangi parolni tasdiqlash")

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'image', 'current_password', 'new_password', 'new_password2', 'password', 'password2']
        read_only_fields = ['id']

    def validate(self, data):
        if not self.instance:
            if not data.get('password', None):
                raise serializers.ValidationError({"password": "To'ldirilishi shart"})
            if not data.get('password2', None):
                raise serializers.ValidationError({"password2": "To'ldirilishi shart"})
            if data['password'] != data['password2']:
                raise serializers.ValidationError({"new_password": "Yangi parollar bir xil emas."})
            return data
        else:
            if 'new_password' in data or 'new_password2' in data:
                if 'current_password' not in data:
                    raise serializers.ValidationError({"current_password": "Parolni yangilash uchun hozirgi parolni kiriting."})

                if data['new_password'] != data['new_password2']:
                    raise serializers.ValidationError({"new_password": "Yangi parollar bir xil emas."})

                user = self.instance
                if not user.check_password(data['current_password']):
                    raise serializers.ValidationError({"current_password": "Amaldagi parol noto'g'ri kiritildi."})
            return data

    def create(self, validated_data):
        validated_data.pop('password2', None)  # password2 ni olib tashlash
        user = User(**validated_data)
        user.set_password(validated_data.pop('password', None))  # password ni o'rnatish
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop('new_password2', None)
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if new_password:
            instance.set_password(new_password)

        instance.save()
        return instance


class CourseSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField(required=False)
    teacher = UserSerializer(required=False)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher_id', 'teacher', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
        extra_kwargs = {'teacher_id': {'write_only': True}}
        depth = 1

    def create(self, validated_data):
        teacher_id = validated_data.pop('teacher_id', None)

        course = Course(**validated_data)

        if teacher_id:
            try:
                course.teacher = User.objects.get(pk=teacher_id)
            except User.DoesNotExist:
                raise serializers.ValidationError({"teacher_id": "Bunday o'qituvchi mavjud emas."})

        course.save()
        return course

    def update(self, instance, validated_data):
        print(validated_data)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.teacher_id = validated_data.get('teacher_id', instance.teacher_id)
        instance.save()
        return instance


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course']
        read_only_fields = ['id']


