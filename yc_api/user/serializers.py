from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    class Meta(object):
        model = User
        fields = ['id','password', 'username', 'token', 'first_name',
                    'last_name', 'top_streak', 'current_streak', 'profile_picture',
                    'last_study_date', 'followers_count', 'following_count'] # I delete the groups
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key
    
    def create(self, validated_data):
        # groups_data = validated_data.pop('groups', [])

        user  =  User.objects.create_user(**validated_data)

        # if not groups_data:
        #     default_groups = Group.objects.get(name='Viewer')
        #     user.groups.add(default_groups)
        # else:
        #     for group in groups_data:
        #         group_obj = Group.objects.get(name=group)
        #         user.groups.add(group_obj)

        token = Token.objects.create(user=user)

        return user


class UserWithStreaksSerailizer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'top_streak', 'current_streak',
                    'profile_picture']
