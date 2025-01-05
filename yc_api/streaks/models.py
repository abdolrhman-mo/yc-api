from django.db import models
from django.contrib.auth.models import User

class Streak(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE, related_name="streaks")
    current_streak=models.IntegerField(default=0)
    top_streak=models.IntegerField(default=0)

    def __str__(self): 
        return f"{self.user.username} - Current: {self.current_streak}, Top: {self.top_streak}"



