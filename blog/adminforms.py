from django import forms

from .models import Post


class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)

    class Meta:
        model = Post
        exclude = ('owner',)