from django import forms
from .models import Post, Category, Tag


class PostForm(forms.ModelForm):
    """Form for users to create/edit blog posts."""
    
    tags_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400',
            'placeholder': 'python, django, web-development (comma-separated)'
        }),
        help_text='Enter tags separated by commas'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'category', 'featured_image', 'excerpt', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400',
                'placeholder': 'Enter your post title'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg text-white file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-cyan-600 file:text-white hover:file:bg-cyan-700'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400',
                'placeholder': 'Brief description of your post (shown in previews)',
                'rows': 3
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400',
                'placeholder': 'Write your post content here...',
                'rows': 15,
                'id': 'id_content'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()
        self.fields['category'].empty_label = "Select a category"
        
        # If editing, populate tags
        if self.instance.pk:
            self.fields['tags_input'].initial = ', '.join(
                tag.name for tag in self.instance.tags.all()
            )

    def save(self, commit=True):
        post = super().save(commit=False)
        
        if commit:
            post.save()
            
            # Handle tags
            self.instance.tags.clear()
            tags_input = self.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    from slugify import slugify
                    tag, created = Tag.objects.get_or_create(
                        slug=slugify(tag_name),
                        defaults={'name': tag_name}
                    )
                    post.tags.add(tag)
        
        return post
