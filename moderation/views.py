from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.utils import timezone
from comments.models import Comment
from blog.models import Post
from accounts.models import User
from notifications.models import Notification
from .models import ModerationLog, UserRestriction


def moderator_required(view_func):
    """Decorator to check if user is a moderator."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not request.user.can_moderate():
            return HttpResponseForbidden('You do not have moderation permissions.')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
@moderator_required
def moderation_dashboard(request):
    """Moderation dashboard showing pending items."""
    pending_comments = Comment.objects.filter(is_approved=False, is_deleted=False)[:20]
    pending_posts = Post.objects.filter(status='pending').select_related('author')[:20]
    recent_logs = ModerationLog.objects.select_related('moderator', 'target_user')[:20]
    active_restrictions = UserRestriction.objects.filter(is_active=True)[:10]
    
    context = {
        'pending_comments': pending_comments,
        'pending_posts': pending_posts,
        'recent_logs': recent_logs,
        'active_restrictions': active_restrictions,
    }
    return render(request, 'moderation/dashboard.html', context)


@login_required
@moderator_required
@require_POST
def approve_comment(request, comment_id):
    """Approve a pending comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='approve_comment',
        target_user=comment.author,
        target_comment=comment,
        target_post=comment.post
    )
    
    messages.success(request, 'Comment approved.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def hide_comment(request, comment_id):
    """Hide a comment from public view."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_hidden = True
    comment.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='hide_comment',
        target_user=comment.author,
        target_comment=comment,
        target_post=comment.post,
        reason=request.POST.get('reason', '')
    )
    
    messages.success(request, 'Comment hidden.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def delete_comment(request, comment_id):
    """Soft delete a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.soft_delete()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='delete_comment',
        target_user=comment.author,
        target_comment=comment,
        target_post=comment.post,
        reason=request.POST.get('reason', '')
    )
    
    messages.success(request, 'Comment deleted.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def lock_thread(request, post_id):
    """Lock comments on a post."""
    post = get_object_or_404(Post, id=post_id)
    post.comments_locked = True
    post.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='lock_thread',
        target_post=post,
        reason=request.POST.get('reason', '')
    )
    
    messages.success(request, 'Thread locked.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def unlock_thread(request, post_id):
    """Unlock comments on a post."""
    post = get_object_or_404(Post, id=post_id)
    post.comments_locked = False
    post.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='unlock_thread',
        target_post=post
    )
    
    messages.success(request, 'Thread unlocked.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def ban_user(request, user_id):
    """Ban a user from commenting."""
    target_user = get_object_or_404(User, id=user_id)
    
    if target_user.is_superuser or target_user.is_site_admin:
        messages.error(request, 'Cannot ban admin users.')
        return redirect('moderation:dashboard')
    
    target_user.is_banned = True
    target_user.ban_reason = request.POST.get('reason', '')
    target_user.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='ban_user',
        target_user=target_user,
        reason=request.POST.get('reason', '')
    )
    
    messages.success(request, f'User {target_user.username} has been banned.')
    return redirect('moderation:dashboard')


@login_required
@moderator_required
@require_POST
def unban_user(request, user_id):
    """Unban a user."""
    target_user = get_object_or_404(User, id=user_id)
    target_user.is_banned = False
    target_user.ban_reason = ''
    target_user.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='unban_user',
        target_user=target_user
    )
    
    messages.success(request, f'User {target_user.username} has been unbanned.')
    return redirect('moderation:dashboard')


@login_required
@moderator_required
@require_POST
def approve_post(request, post_id):
    """Approve a pending blog post."""
    post = get_object_or_404(Post, id=post_id)
    post.status = 'published'
    post.published_at = timezone.now()
    post.save()
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='approve_post',
        target_user=post.author,
        target_post=post
    )
    
    # Notify the author
    Notification.create_post_published(post)
    
    messages.success(request, f'Post "{post.title}" has been approved and published.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))


@login_required
@moderator_required
@require_POST
def reject_post(request, post_id):
    """Reject a pending blog post."""
    post = get_object_or_404(Post, id=post_id)
    post.status = 'rejected'
    post.save()
    
    reason = request.POST.get('reason', '')
    
    ModerationLog.objects.create(
        moderator=request.user,
        action='reject_post',
        target_user=post.author,
        target_post=post,
        reason=reason
    )
    
    # Notify the author
    Notification.create_post_rejected(post, reason)
    
    messages.success(request, f'Post "{post.title}" has been rejected.')
    return redirect(request.META.get('HTTP_REFERER', 'moderation:dashboard'))
