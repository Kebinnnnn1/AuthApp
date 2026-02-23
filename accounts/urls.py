from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('verify-email/', views.verify_email_view, name='verify_email'),
    path('resend-code/', views.resend_code_view, name='resend_code'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('admin-panel/', views.admin_panel_view, name='admin_panel'),
]
