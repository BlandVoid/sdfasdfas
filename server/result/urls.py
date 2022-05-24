from django.urls import path

from .views import ResultAPIView

# InfoAPIView,

urlpatterns = [
    path("", ResultAPIView.as_view(), name="result"),
    # path("info/", InfoAPIView.as_view(), name="result-info"),
]
