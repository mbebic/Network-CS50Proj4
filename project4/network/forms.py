from django import forms
from .models import Post

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': ''
        }
        widgets = {
        'content': forms.Textarea(attrs={'rows':3, 'maxlength': 1000, 'class': 'form-control', 'placeholder': 'What is on your mind?'})
        }