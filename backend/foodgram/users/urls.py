from django.urls import include, path

from djoser import views
from users.views import FollowApiView, ListFollowViewSet

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowApiView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', ListFollowViewSet.as_view(),
         name='subscription'),
    path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', views.TokenDestroyView.as_view(),
         name='logout'),
    path('', include('djoser.urls')),
]










# from django.urls import include, path
# from djoser import views

# from users.views import CustomUserViewSet

# urlpatterns = [
#     path('users/<int:id>/subscribe/', CustomUserViewSet,
#          name='subscribe'),
#     path('users/subscriptions/', CustomUserViewSet,
#          name='subscription'),
#     path('auth/token/login/', views.TokenCreateView.as_view(), name='login'),
#     path('auth/token/logout/', views.TokenDestroyView.as_view(),
#          name='logout'),
#     path('', include('djoser.urls')),
# ]
