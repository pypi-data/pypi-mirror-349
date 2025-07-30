from rest_framework import serializers
from .models import CustomUser, RbacTasks, Organisation

class CustomUserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'roles', 'first_name', 'last_name']

    def get_roles(self, obj):
        return obj.get_roles_array()

class RbacTasksSerilizer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = RbacTasks
        fields = ['task', 'roles', 'id']

    def get_roles(self, obj):
        return obj.get_roles_array()


class OrganisationsSerializer(serializers.ModelSerializer):
    admin = CustomUserSerializer(read_only=True)
    class Meta:
        model = Organisation
        fields = ['id', 'name', 'primaryPhoneNumber', 'admin']
