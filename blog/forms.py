from django import forms
from blog.models import Post, Comment  # Imported models to use connect them with forms.


class PostForm(forms.ModelForm):
    """
    Forms for posts.
    """
    class Meta:
        model = Post
        fields = ('author', 'title', 'text')  # Form elements to show. 'author' can be changed by an admin.

        # 'widget' specifies the attributes (even for css) of the forms.
        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        }


class CommentForm(forms.ModelForm):
    """
    Forms for comments.
    """
    class Meta:
        model = Comment
        fields = ('author', 'text')  # Form elements to show. 'author' can be changed by an admin.

        # 'widget' specifies the attributes (even for css) of the forms.
        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'})
        }
