from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

UserModel = get_user_model()


class Topic(models.Model):
    objects = models.Manager()

    name = models.CharField(
        max_length=25,
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        max_length=50,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    objects = models.Manager()

    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        unique=True,
    )

    body = models.TextField(
        null=False,
        blank=False,
    )

    slug = models.SlugField(
        max_length=250,
        null=False,
        blank=False,
        editable=False,
        unique=True,
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
    )

    publish = models.DateTimeField(
        default=timezone.now,
    )

    created = models.DateTimeField(
        auto_now_add=True,
    )

    updated = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    objects = models.Manager()
    body = models.TextField(
        null=False,
        blank=False,
    )

    created = models.DateTimeField(
        default=timezone.now
    )

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
    )

    # def __str__(self):
    #     return self.body[:50]


class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
    )

    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        null=True,
    )

    def __str__(self):
        return f'Liked by {self.user.user_name}'
