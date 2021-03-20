from django.urls import path
from .views import *

urlpatterns = [
    path('slot/',									all_slots,				name='slots'),
    path('slot/add',								create_slot,			name='slot_add'),
    path('time/<int:pk>',							time_sel,				name='time_sel'),
]
