from django.urls import path
from .views import PostList, PostCreateView, PostDetailView, PostLikeView

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:pk>/like/', PostLikeView.as_view(), name='post-like'),
]