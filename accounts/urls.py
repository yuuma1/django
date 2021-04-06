from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name="create"),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('change/', views.UserChangeView.as_view(), name="change"),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), 
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'), 
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), 
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), 
]
