from django.urls import path, include
from rest_framework import routers
from .views import LoginView, UserCreateView, AccountView, CaseView, CaseLinkView, IncidentView

router = routers.DefaultRouter()
router.register('accounts', AccountView)
router.register('cases', CaseView)
router.register('incidents', IncidentView)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserCreateView.as_view()),
    path('login', LoginView.as_view()),
    path('caselinks', CaseLinkView.as_view())
]