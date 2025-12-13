from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400 transition-colors',
            'placeholder': 'John Doe'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400 transition-colors',
            'placeholder': 'you@example.com'
        })
        self.fields['subject'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400 transition-colors',
            'placeholder': 'How can I help you?'
        })
        self.fields['message'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg focus:ring-2 focus:ring-cyan-500 focus:border-transparent text-white placeholder-gray-400 transition-colors',
            'placeholder': 'Hi Albin, I\'d like to discuss a project...',
            'rows': 5
        })
