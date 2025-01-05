from django.shortcuts import render
from rest_framework.decorators import api_view  
from rest_framework.response import Response  
from .models import Streak
@api_view(['GET'])
def get_streak(request):
    streaks = Streak.objects.filter(user=request.user)  
    data = [{"current_streak": streak.current_streak, "top_streak": streak.top_streak} for streak in streaks]
    return Response(data)  

@api_view(['POST']) 
def start_streak(request):
    streak, created = Streak.objects.get_or_create(user=request.user)  #
    streak.current_streak = 1  
    streak.save()  
    return Response({"message": "Streak started!", "current_streak": streak.current_streak})

@api_view(['PUT']) 
def increment_streak(request):
    try:
        streak = Streak.objects.get(user=request.user)  
        streak.current_streak += 1  
        if streak.current_streak > streak.top_streak:
            streak.top_streak = streak.current_streak  
        streak.save()  
        return Response({"message": "Streak incremented!", "current_streak": streak.current_streak})
    except Streak.DoesNotExist:
        return Response({"error": "Streak not found"}, status=404)