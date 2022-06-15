from django.urls import path, include
from . import views
from Users.views import ObtainAuthToken

# A list of urls that will be used in the project.
urlpatterns = [
    path('', views.index),
    path("invoices/", views.InvoiceListAPIView.as_view()),
    path("invoices/new/", views.InvoiceCreateAPIView.as_view()),
    path("invoices/<int:pk>/", views.InvoiceDetailAPIView.as_view()),
    path("additional-services/", views.AdditionalServicesListAPIView.as_view()),
    path('analytics/', views.AnalyticsViewSet.as_view(), name='analytic'),
    path("additional-services/<int:pk>/",
         views.AdditionalServicesDetailAPIView.as_view()),
    path('wash-types/', views.WashTypeListAPIView.as_view()),
    path('wash-types/<int:pk>/', views.WashTypeDetailAPIView.as_view()),
    path('users/', include('Users.urls')),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='api_token_auth'),
]
