from django.urls import path
from .views import HelloView, HelloAgainView, health_check

urlpatterns = [
    path("", health_check),
    path("hello", HelloView.as_view(), name="hello"),
    path("hello/again", HelloAgainView.as_view(), name="hello-again"),
]
