from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='user-profile'),
    path('activate/', views.ActivateAccountView.as_view(), name='activate_account'),
]
