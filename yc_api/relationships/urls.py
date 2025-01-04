from django.urls import path
from .views import RelationshipViewSet

urlpatterns = [
    path('followers/', RelationshipViewSet.as_view({'get': 'followers'}), name='followers'),
    path('following/', RelationshipViewSet.as_view({'get': 'following'}), name='following'),
    path('follow/', RelationshipViewSet.as_view({'post': 'follow'}), name='follow'),
    path('unfollow/', RelationshipViewSet.as_view({'delete': 'unfollow'}), name='unfollow'),
]
