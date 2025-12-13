from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from .models import Post, Category, Tag


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
