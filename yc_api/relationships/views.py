from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Relationship
from .serializers import RelationshipSerializer

class RelationshipViewSet(viewsets.ModelViewSet):
    queryset = Relationship.objects.all()
    serializer_class = RelationshipSerializer

    def followers(self, request, *args, **kwargs):
        """ Get followers of the authenticated user """
        user = request.user
        followers = Relationship.objects.filter(following=user)
        serializer = RelationshipSerializer(followers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def following(self, request, *args, **kwargs):
        """ Get the users that the authenticated user is following """
        user = request.user
        following = Relationship.objects.filter(follower=user)
        serializer = RelationshipSerializer(following, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def follow(self, request, *args, **kwargs):
        """ Create a new relationship (follow a user) """
        follower_id = request.data.get('follower_id')
        following_id = request.data.get('following_id')

        if not follower_id or not following_id:
            return Response({"error": "follower_id and following_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        if follower_id == following_id:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if Relationship.objects.filter(follower=follower_id, following=following_id).exists():
            return Response({"error": "Relationship already exists"}, status=status.HTTP_400_BAD_REQUEST)

        Relationship.objects.create(follower_id=follower_id, following_id=following_id)
        return Response({"message": "Followed successfully"}, status=status.HTTP_201_CREATED)

    def unfollow(self, request, *args, **kwargs):
        """ Delete a relationship (unfollow a user) """
        follower_id = request.data.get('follower_id')
        following_id = request.data.get('following_id')

        if not follower_id or not following_id:
            return Response({"error": "follower_id and following_id are required"}, status=status.HTTP_400_BAD_REQUEST)

        relationship = Relationship.objects.filter(follower=follower_id, following=following_id).first()

        if not relationship:
            return Response({"error": "Relationship does not exist"}, status=status.HTTP_404_NOT_FOUND)

        relationship.delete()
        return Response({"message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
