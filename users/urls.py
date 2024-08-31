from django.contrib.auth import views as auth_views
from django.urls import path
from .views import (
    RegisterView,
    EmailVerificationView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView,
    LoginView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify-email/<int:user_id>/<str:token>/', EmailVerificationView.as_view(), name='verify_email'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),  # Новый URL
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]