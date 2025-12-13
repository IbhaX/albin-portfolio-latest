from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.utils import timezone
from .models import Post, Category, Tag
from .forms import PostForm


def post_list(request):
    """List all published blog posts."""
    posts = Post.objects.filter(status='published').select_related('author', 'category')
    
    # Search
    query = request.GET.get('q')
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query)
        )
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'categories': Category.objects.all(),
        'tags': Tag.objects.all(),
        'query': query,
    }
    return render(request, 'blog/post_list.html', context)


def post_detail(request, slug):
    """Display a single blog post with comments."""
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    
    # Get approved comments as a tree
    comments = post.comments.filter(is_approved=True).select_related('author')
    
    context = {
        'post': post,
        'comments': comments,
    }
    return render(request, 'blog/post_detail.html', context)


def category_posts(request, slug):
    """List posts by category."""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status='published', category=category)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'category': category,
        'posts': posts,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/category_posts.html', context)


def tag_posts(request, slug):
    """List posts by tag."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status='published', tags=tag)
    
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'tag': tag,
        'posts': posts,
        'tags': Tag.objects.all(),
    }
    return render(request, 'blog/tag_posts.html', context)


@login_required
def create_post(request):
    """Allow logged-in users to create a new blog post."""
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.status = 'pending'  # Requires approval
            post.save()
            form.save()  # Save tags
            messages.success(request, 'Your post has been submitted for review. It will be visible after approval.')
            return redirect('blog:my_posts')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/create_post.html', context)


@login_required
def edit_post(request, slug):
    """Allow users to edit their own posts (if not published)."""
    post = get_object_or_404(Post, slug=slug)
    
    if not post.can_edit(request.user):
        return HttpResponseForbidden('You cannot edit this post.')
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            # If editing a rejected post, set back to pending
            if post.status == 'rejected':
                post.status = 'pending'
            post.save()
            form.save()  # Save tags
            messages.success(request, 'Your post has been updated.')
            return redirect('blog:my_posts')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'categories': Category.objects.all(),
    }
    return render(request, 'blog/edit_post.html', context)


@login_required
def delete_post(request, slug):
    """Allow users to delete their own posts."""
    post = get_object_or_404(Post, slug=slug)
    
    if not post.can_delete(request.user):
        return HttpResponseForbidden('You cannot delete this post.')
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted.')
        return redirect('blog:my_posts')
    
    return render(request, 'blog/delete_post.html', {'post': post})


@login_required
def my_posts(request):
    """Show user's own posts with their status."""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'blog/my_posts.html', context)
