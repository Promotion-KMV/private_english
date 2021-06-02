from django.urls import path, include
from .views import *


app_name = 'account'

urlpatterns = [

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('activate/<uidb64>/<token>', VerificationView.as_view(), name='activate'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', ResetPasswordCompleteView.as_view(), name='password_reset_complete')
]