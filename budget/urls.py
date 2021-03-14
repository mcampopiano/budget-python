from django.conf.urls import include
from django.urls import path
from budgetapi.views import register_user, login_user
from rest_framework import routers
from budgetapi.views import Budgets, Envelopes, Deposits

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'budgets', Budgets, 'budget')
router.register(r'envelopes', Envelopes, 'envelope')
router.register(r'deposits', Deposits, 'deposit')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]