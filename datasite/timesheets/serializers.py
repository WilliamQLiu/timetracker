""" Used in Django REST Framework """

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from timesheets.models import Time, CostCode, Program, UserProfile, Department, JobType


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class UserProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = UserProfile
        fields = ['department', 'salary']


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'email', 'userprofile')


class TimeSerializer(serializers.ModelSerializer):
    #fields = ('url', 'username', 'email', 'groups')
    user = UserSerializer()

    class Meta:
        model = Time
        fields = ['date_select', 'user']


class CostCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostCode
        fields = ['program_name']


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        #fields = ('hours_spent', 'minutes_spent')
        depth = 2


class RelatedUserField(serializers.RelatedField):
    read_only = True

    def from_native(self, data):
        return User.objects.get(email=data)


class DataSerializer(serializers.ModelSerializer):
    time = TimeSerializer(read_only=True)
    program_select = CostCodeSerializer(read_only=True)

    class Meta:
        model = Program
        fields = ('hours_spent', 'minutes_spent', 'time', 'program_select')

'''
class DataSerializer(serializers.ModelSerializer):
    time = serializers.SlugRelatedField(
        read_only=True, slug_field='date_select')
    program_select = serializers.SlugRelatedField(
        read_only=True, slug_field='cost_code')
    #username = serializers.SlugRelatedField(
    #    read_only=True, slug_field='users')
    #username = RelatedUserField(many=False)

    class Meta:
        model = Program
        fields = ('hours_spent', 'minutes_spent', 'time', 'program_select')
'''



