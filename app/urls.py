from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_activity, name='add_activity'),
    path('history/', views.activity_history, name='history'),
    path('activity/<int:pk>/', views.activity_detail, name='activity_detail'),
    path('delete/<int:pk>/', views.delete_activity, name='delete_activity'),
]
