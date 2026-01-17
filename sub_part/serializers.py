from rest_framework import serializers
from .models import Company1, StudentAdmission, User, Employee, UserSubscription ,SchoolRegistration, Notification

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolRegistration
        fields = "__all__"

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company1
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "school",
            "email",
            'first_name',
            'last_name',
            "username",
            "password",
            "buyer_id",
            'is_school_admin',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"

class StudentAdmisssionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAdmission
        fields = "__all__"