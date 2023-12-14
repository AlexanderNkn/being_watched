from rest_framework.routers import DefaultRouter

from . import views
from .apps import LinksConfig

app_name = LinksConfig.name

router = DefaultRouter()
router.register('', views.VisitedLinkViewSet)

urlpatterns = [
    *router.urls
]
