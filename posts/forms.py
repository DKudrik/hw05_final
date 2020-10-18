from django import forms

from django.db import models
from django.forms import ModelForm
from .models import Comment, Post
from django.utils.translation import gettext_lazy as _


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "text",
            "group",
            "image",
        ]
        labels = {
            "text": _("Введите текст поста"),
            "group": _("Выберите группу(при необходимости)"),
        }
    text = forms.CharField(widget=forms.Textarea)


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text", ]
        labels = {"text": _("Введите текст комментария"), }
    text = forms.CharField(widget=forms.Textarea)
