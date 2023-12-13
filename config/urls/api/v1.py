from django.urls import include, path

urlpatterns = [
    path('links/', include('apps.links.urls')),
]
