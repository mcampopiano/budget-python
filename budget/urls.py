from django.conf.urls import include
from django.urls import path
from budgetapi.views import register_user, login_user

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]