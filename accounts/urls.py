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
    path('admin-panel/promote/<int:user_id>/', views.promote_user_view, name='promote_user'),
    path('admin-panel/demote/<int:user_id>/', views.demote_user_view, name='demote_user'),
    path('admin-panel/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('admin-panel/disable/<int:user_id>/', views.disable_user_view, name='disable_user'),
    path('admin-panel/enable/<int:user_id>/', views.enable_user_view, name='enable_user'),
    # Game
    path('game/', views.game_view, name='game'),
    path('game/submit/', views.submit_score_view, name='submit_score'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    # Diagnostic (temp)
    path('debug/status/', views.debug_status_view, name='debug_status'),
]


