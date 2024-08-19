from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django_app.users.views import AuthViewSet
from django_app.users.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("auth", AuthViewSet, basename="auth")


app_name = "api"
urlpatterns = router.urls
