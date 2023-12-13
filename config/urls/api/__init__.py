from django.urls import include, path

urlpatterns = [
    path('v1/', include('config.urls.api.v1')),
]
