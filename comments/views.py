from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from blog.models import Post
from notifications.models import Notification
from .models import Comment
from .forms import CommentForm


@login_required
@require_POST
def add_comment(request, post_slug):
    """Add a new comment to a post."""
    post = get_object_or_404(Post, slug=post_slug, status='published')
    
    if not post.allow_comments or post.comments_locked:
        messages.error(request, 'Comments are not allowed on this post.')
        return redirect('blog:post_detail', slug=post_slug)
    
    if not request.user.can_comment():
        messages.error(request, 'You do not have permission to comment.')
        return redirect('blog:post_detail', slug=post_slug)
    
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.author = request.user
        
        # Handle reply
        parent_id = request.POST.get('parent_id')
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id, post=post)
            comment.parent = parent
        
        comment.save()
        
        # Create notifications
        if comment.parent:
            # Reply to a comment - notify parent comment author
            Notification.create_comment_reply(comment)
        else:
            # New comment on post - notify post author
            Notification.create_new_comment(comment)
        
        messages.success(request, 'Comment posted successfully.')
    else:
        messages.error(request, 'Error posting comment.')
    
    return redirect('blog:post_detail', slug=post_slug)


@login_required
@require_POST
def edit_comment(request, comment_id):
    """Edit an existing comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if not comment.can_edit(request.user):
        return HttpResponseForbidden('You cannot edit this comment.')
    
    form = CommentForm(request.POST, instance=comment)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.edited_at = timezone.now()
        comment.save()
        messages.success(request, 'Comment updated.')
    
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
@require_POST
def delete_comment(request, comment_id):
    """Soft delete a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if not comment.can_delete(request.user):
        return HttpResponseForbidden('You cannot delete this comment.')
    
    comment.soft_delete()
    messages.success(request, 'Comment deleted.')
    
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def reply_form(request, comment_id):
    """HTMX endpoint to get reply form."""
    comment = get_object_or_404(Comment, id=comment_id)
    
    if not comment.can_reply(request.user):
        return HttpResponseForbidden('You cannot reply to this comment.')
    
    form = CommentForm()
    return render(request, 'comments/partials/reply_form.html', {
        'form': form,
        'parent': comment
    })
