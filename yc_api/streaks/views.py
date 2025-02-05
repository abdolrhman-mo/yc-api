from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Streak, StudyLog
from .serializers import StreakSerializer, StudyLogSerializer
from datetime import date, timedelta
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

class StreakViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """ ViewSet to handle streak-related operations """

    queryset = Streak.objects.all()
    serializer_class = StreakSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get_serializer_class(self):
        if self.action == 'list':
            return StreakSerializer
        return StudyLogSerializer
    def get_queryset(self):
        """ Return streaks only for the authenticated user """
        return Streak.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='increment')
    def increment_streak(self, request):
        """ Increment user's streak based on daily study """
        user = request.user
        duration = request.data.get("duration")

        if not duration or int(duration) < 25:
            return Response({"error": "Study session must be at least 25 minutes."}, status=status.HTTP_400_BAD_REQUEST)

        today = date.today()

        # Log the study session
        StudyLog.objects.create(user=user, study_date=today, duration=duration)

        # Retrieve or create the user's streak
        streak, created = Streak.objects.get_or_create(user=user, defaults={
            'last_study_date': today,
            'current_streak': 1,
            'top_streak': 1
        })

        if not created:
            if streak.last_study_date == today:
                # Already studied today, no streak increment needed
                pass
            elif streak.last_study_date == today - timedelta(days=1):
                # Consecutive day, increment the streak
                streak.current_streak += 1
            else:
                # Missed a day, reset the current streak
                streak.current_streak = 1

            # Update top streak if current streak exceeds it
            if streak.current_streak > streak.top_streak:
                streak.top_streak = streak.current_streak

            streak.last_study_date = today
            streak.save()

        # Update user's current and top streaks
        user.current_streak = streak.current_streak
        user.top_streak = streak.top_streak
        user.last_study_date = streak.last_study_date
        user.save()

        serializer = StreakSerializer(streak)
        return Response(serializer.data, status=status.HTTP_200_OK)
