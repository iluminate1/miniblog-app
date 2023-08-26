from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )
    content = models.TextField(blank=True, verbose_name="Content")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="IMG")
    link = models.URLField(blank=True, unique=True, verbose_name="Link")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Create time")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Edit time")
    is_published = models.BooleanField(default=True, verbose_name="Is Published")
    cat = models.ForeignKey(
        "Category", on_delete=models.PROTECT, verbose_name="Category"
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Item's"
        ordering = ["-time_update"]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category")
    slug = models.SlugField(
        max_length=255, unique=True, db_index=True, verbose_name="URL"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", kwargs={"cat_slug": self.slug})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["id"]

class FeedBack(models.Model):
    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='User'
    )
    first_name = models.CharField(max_length=125, verbose_name='First name')
    last_name = models.CharField(max_length=125, verbose_name='Last name')
    email = models.EmailField(verbose_name='Email')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Create time")
    content = models.TextField(max_length=255, verbose_name='Message')

    def __str__(self):
        return self.user