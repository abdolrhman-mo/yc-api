from django.db import models
from user.models import User

class Relationship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate relationships
