from django.urls import path
from rest_framework import routers
from .views import InvitationView


routes = routers.DefaultRouter()
routes.register(r"", InvitationView, basename="invitation")

urlpatterns = []
urlpatterns += routes.urls
