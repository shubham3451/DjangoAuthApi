from django.urls import path
from api.views import UserRegisterView, userLoginView, UserProfileView, UserChangepasswordView, UserSendPasswordResetMailView, userpasswordresetview

urlpatterns = [
    path('register/',UserRegisterView.as_view(), name='register'),
    path('login/',userLoginView.as_view(), name='login'),
    path('profile/',UserProfileView.as_view(), name='profile'),
    path('change password/',UserChangepasswordView.as_view(),name='change password'),
    path('sendresetlink/',UserSendPasswordResetMailView.as_view(),name='sendresetlink'),
    path('reset-password/<uid>/<token>/', userpasswordresetview.as_view(), name='reset-password'),

]