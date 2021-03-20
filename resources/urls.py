from django.urls import path
from .views import *

urlpatterns = [
    path('resources/',								all_subs,			name='resources'),
]
