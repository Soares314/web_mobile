from django.urls import path, include
from users.views import *

urlpatterns = [
    path('', Login.as_view(), name='login'),
]
