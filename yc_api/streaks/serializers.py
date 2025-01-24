from rest_framework import serializers
from .models import Streak, StudyLog

class StreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = Streak
        fields = ['id', 'user', 'current_streak', 'top_streak']
        read_only_fields = ['id', 'user', 'current_streak', 'top_streak']  # Prevent updates to these fields

class StudyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyLog
        fields = ['id', 'user', 'study_date', 'duration']
        read_only_fields = ['id', 'user', 'study_date']  # `study_date` is automatically set
