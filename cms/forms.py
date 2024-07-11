from django import forms
from .models import Article

class QuillEditor(forms.Textarea):
    template_name = 'widgets/quill_editor.html'

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'published']

        widgets = {
            'content': QuillEditor(),
        }