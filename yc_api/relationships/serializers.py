from rest_framework import serializers
from .models import Relationship
from user.models import User
from user.serializers import UserSerializer
class RelationshipSerializer(serializers.ModelSerializer):
    # Use source='follower_id' and source='following_id' to map input fields to model fields
    # follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    follower = UserSerializer(read_only=True,many=False)
    following = UserSerializer(read_only=True,many=False)

    class Meta:
        model = Relationship
        fields = ['follower', 'following', 'created_at']  # Include only necessary fields
