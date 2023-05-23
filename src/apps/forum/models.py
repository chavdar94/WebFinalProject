from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify

UserModel = get_user_model()


class Topic(models.Model):
    objects = models.Manager()

    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    objects = models.Manager()
    published = PublishedManager()

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(
        max_length=50,
        null=False,
        blank=False,
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

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
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

    def __str__(self):
        return self.body[:50]
