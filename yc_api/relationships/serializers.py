from rest_framework import serializers
from .models import Relationship
from user.models import User

class RelationshipSerializer(serializers.ModelSerializer):
    # Use source='follower_id' and source='following_id' to map input fields to model fields
    follower = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Relationship
        fields = ['follower', 'following', 'created_at']  # Include only necessary fields
