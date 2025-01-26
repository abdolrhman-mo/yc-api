from django.shortcuts import render
from rest_framework.decorators import api_view  
from rest_framework.response import Response  
from .models import Streak,StudyLog
from datetime import date, timedelta
from .serializers import StreakSerializer
@api_view(['GET'])
def get_streak(request):
    streaks = Streak.objects.filter(user=request.user)  
    serializer = StreakSerializer(streaks, many=True)
    return Response(serializer.data) 

@api_view(['POST']) 
def start_streak(request):
    streak, created = Streak.objects.get_or_create(user=request.user)  #
    streak.current_streak = 0  
    streak.save()  
    serializer = StreakSerializer(streak)
    return Response(serializer.data)
@api_view(['POST']) 
def increment_streak(request):
    try:
        # Get the duration from the frontend (in minutes)
        duration = request.data.get("duration", 0)

        if duration < 25:
            # Reject the session if it's less than 25 minutes
            return Response({"error": "Study session must be at least 25 minutes."}, status=400)

        # Log the study session
        StudyLog.objects.create(user=request.user, study_date=date.today(), duration=duration)

        # Handle streak logic
        streak = Streak.objects.get(user=request.user)
        today = date.today()

        if streak.last_study_date == today:
            # Do nothing and silently return the current streak
            return Response({"current_streak": streak.current_streak})

        if streak.last_study_date == today - timedelta(days=1):
            streak.current_streak += 1
        else:
            #gap
            streak.current_streak = 1

        if streak.current_streak > streak.top_streak:
            streak.top_streak = streak.current_streak

        streak.last_study_date = today
        streak.save()
        serializer = StreakSerializer(streak)
        return Response(serializer.data)
    except Streak.DoesNotExist:
        return Response({"error": "Streak not found"}, status=404)