from django.urls import path
from . import views

app_name = 'moderation'

urlpatterns = [
    path('', views.moderation_dashboard, name='dashboard'),
    path('comment/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('comment/<int:comment_id>/hide/', views.hide_comment, name='hide_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('post/<int:post_id>/lock/', views.lock_thread, name='lock_thread'),
    path('post/<int:post_id>/unlock/', views.unlock_thread, name='unlock_thread'),
    path('post/<int:post_id>/approve/', views.approve_post, name='approve_post'),
    path('post/<int:post_id>/reject/', views.reject_post, name='reject_post'),
    path('user/<int:user_id>/ban/', views.ban_user, name='ban_user'),
    path('user/<int:user_id>/unban/', views.unban_user, name='unban_user'),
]
