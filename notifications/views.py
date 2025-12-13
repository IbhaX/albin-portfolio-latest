from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification


@login_required
def notification_list(request):
    """Display all notifications for the user."""
    notifications = request.user.notifications.all()[:50]
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'notifications/list.html', context)


@login_required
def notifications_dropdown(request):
    """Get recent notifications for dropdown (AJAX)."""
    notifications = request.user.notifications.all()[:10]
    unread_count = request.user.notifications.filter(is_read=False).count()
    
    data = {
        'unread_count': unread_count,
        'notifications': [
            {
                'id': n.id,
                'title': n.title,
                'message': n.message[:80] + ('...' if len(n.message) > 80 else ''),
                'type': n.notification_type,
                'is_read': n.is_read,
                'url': n.get_url(),
                'created_at': n.created_at.strftime('%b %d, %H:%M'),
                'sender': n.sender.username if n.sender else None,
            }
            for n in notifications
        ]
    }
    return JsonResponse(data)


@login_required
@require_POST
def mark_as_read(request, notification_id):
    """Mark a single notification as read."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.is_read = True
    notification.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('notifications:list')


@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read."""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('notifications:list')


@login_required
@require_POST
def delete_notification(request, notification_id):
    """Delete a notification."""
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True})
    return redirect('notifications:list')
