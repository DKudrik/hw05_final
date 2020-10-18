from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="Адрес")
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.title


class Post(models.Model):
    class Meta:
        ordering = ("-pub_date", )
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    text = models.TextField(verbose_name="Текст")
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
        )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Автор",
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="posts",
        verbose_name="Группа"
    )
    image = models.ImageField(
        upload_to="posts/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return (f'pk={self.pk} author={self.author} group={self.group} '
                f'date={self.pub_date} {self.text[:70]}')


class Comment(models.Model):
    class Meta:
        ordering = ("-created", )
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Запись",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор",
    )
    text = models.TextField(verbose_name="Текст")
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата публикации",
    )


class Follow(models.Model):
    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик",
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Автор",
    )
