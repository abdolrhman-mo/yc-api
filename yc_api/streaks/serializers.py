from rest_framework import serializers
from .models import Streak, StudySession

class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = ['id', 'user', 'current_streak', 'top_streak', 'last_study_date']
        read_only_fields = ['id', 'user', 'current_streak', 'top_streak']  # Prevent updates to these fields

class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = ['id', 'user', 'study_date', 'duration']
        read_only_fields = ['id', 'user', 'study_date']  # `study_date` is automatically set
