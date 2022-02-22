from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListAPIView.as_view()),
    path('create/', views.UserCreateAPIView.as_view()),
    path('<int:pk>/', views.UserDetailAPIView.as_view()),
]
