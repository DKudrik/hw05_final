from django import forms
from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import Comment, Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            "text",
            "group",
            "image",
        ]
        labels = {
            "group": _("Выберите группу(при необходимости)"),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text", ]
        labels = {"text": _("Введите текст комментария"), }
    text = forms.CharField(widget=forms.Textarea)
