# from django.urls import path
# from . import views

from rest_framework.routers import DefaultRouter
from .views import StreakViewSet

router = DefaultRouter()
router.register(r'', StreakViewSet, basename='streak')

urlpatterns = router.urls


# urlpatterns = [
#     path("",views.get_streak,name="get_streak"),     
#     # path('start/', views.start_streak, name='start_streak'),  # Start a streak
#     # /endSession/
#     path('increment/', views.increment_streak, name='increment_streak'),  # Increment strea
# ]