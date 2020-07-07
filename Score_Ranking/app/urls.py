
from django.urls import path, include
from .views import *

urlpatterns = [
    path('score/',Score.as_view()),
]
