from django.urls import path
from . import views

urlpatterns = [
    path("",views.get_streak,name="get_streak"),     
    path('start/', views.start_streak, name='start_streak'),  # Start a streak
    path('increment/', views.increment_streak, name='increment_streak'),  # Increment strea
]