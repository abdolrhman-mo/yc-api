from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Streak, StudyLog
from .serializers import StreakSerializer, StudyLogSerializer
from datetime import date, timedelta

class StreakViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """ ViewSet to handle streak-related operations """

    queryset = Streak.objects.all()
    serializer_class = StreakSerializer

    def get_serializer_class(self):
        if self.action == 'list':
            return StreakSerializer
        return StudyLogSerializer
    def get_queryset(self):
        """ Return streaks only for the authenticated user """
        return Streak.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='increment')
    def increment_streak(self, request):
        """ Increment user's streak based on study session duration """

        try:
            # Get the duration from the frontend (in minutes)
            duration = request.data.get("duration", 0)

            if duration < 25:
                return Response({"error": "Study session must be at least 25 minutes."}, status=status.HTTP_400_BAD_REQUEST)

            # Log the study session
            StudyLog.objects.create(user=request.user, study_date=date.today(), duration=duration)

            # Handle streak logic
            streak = self.get_queryset().first()

            if not streak:
                streak = Streak.objects.create(user=request.user, last_study_date=date.today(), top_streak=1, current_streak=1)
                # return Response({"error": "Streak not found"}, status=status.HTTP_404_NOT_FOUND)

            today = date.today()

            if streak.last_study_date == today:
                # print(streak.last_study_date - today)
                return Response({"current_streak ": streak.current_streak}, status=status.HTTP_200_OK)

            if today - timedelta(days=1) == streak.last_study_date :
                streak.current_streak += 1
            else:
                # Gap in streak
                streak.current_streak = 1

            if streak.current_streak > streak.top_streak:
                streak.top_streak = streak.current_streak

            streak.last_study_date = today
            streak.save()
            serializer = StreakSerializer(streak)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Streak.DoesNotExist:
            return Response({"error": "Streak not found"}, status=status.HTTP_404_NOT_FOUND)
