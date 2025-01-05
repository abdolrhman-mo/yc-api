from django.urls import path
from . import views

urlpatterns = [
    path("streak/",views.get_streak,name="get_streak"),     
    path('streak/start/', views.start_streak, name='start_streak'),  # Start a streak
    path('streak/increment/', views.increment_streak, name='increment_streak'),  # Increment strea
]