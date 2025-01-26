from django.db import models
from user.models import User
from datetime import date, timedelta

class Streak(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="streaks")
    current_streak=models.IntegerField(default=0)
    top_streak=models.IntegerField(default=0)

    def __str__(self): 
        return f"{self.user.username} - Current: {self.current_streak}, Top: {self.top_streak}"

class StudyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="study_logs")
    study_date = models.DateField(default=date.today)  
    duration = models.IntegerField()  
    def __str__(self): 
        return f"{self.user.username} - Current: {self.current_streak}, Top: {self.top_streak}"

