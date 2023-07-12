from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserSignupView, CustomTokenObtainPairView, UserDetailView

urlpatterns = [
    path('signup', UserSignupView.as_view(), name='signup'),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh-token', TokenRefreshView.as_view(), name='refresh-token'),
    path('', UserDetailView.as_view(), name='user-detail'),
]