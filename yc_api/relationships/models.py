from django.db import models, transaction
from django.core.exceptions import ValidationError
from user.models import User

class RelationshipManager(models.Manager):
    def create(self, follower_id, following_id, *args, **kwargs):
        # Fetch user instances from the database
        follower = User.objects.get(id=follower_id)
        following = User.objects.get(id=following_id)

        if follower == following:
            raise ValidationError("You cannot follow yourself.")

        with transaction.atomic():  # Ensures atomicity
            # Create the relationship
            relationship = super().create(follower=follower, following=following, *args, **kwargs)

            # Update followers_count and following_count
            follower.following_count = models.F('following_count') + 1
            following.followers_count = models.F('followers_count') + 1

            follower.save(update_fields=['following_count'])
            following.save(update_fields=['followers_count'])

        return relationship


class Relationship(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()  # Use the custom manager

    def delete(self, *args, **kwargs):
        """Ensure followers_count and following_count are decremented on unfollow."""
        with transaction.atomic():
            # Decrement counts before deletion
            self.follower.following_count = models.F('following_count') - 1
            self.following.followers_count = models.F('followers_count') - 1

            self.follower.save(update_fields=['following_count'])
            self.following.save(update_fields=['followers_count'])

            super().delete(*args, **kwargs)  # Call the original delete method


    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"

    class Meta:
        unique_together = ('follower', 'following')  # Prevent duplicate relationships
