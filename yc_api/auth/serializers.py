from rest_framework import serializers
from yc_api.settings import AUTH_USER_MODEL as User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined'] 
