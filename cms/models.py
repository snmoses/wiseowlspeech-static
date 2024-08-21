from django.core.exceptions import ValidationError
from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class SingletonModel(models.Model):
    """
    this class limits models to having a single instance
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("There can be only one instance of this.")
        return super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def get_instance(cls):
        instance, created = cls.objects.get_or_create(pk=1)
        return instance


class UserContent(models.Model):
    content = QuillField()
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.content.html


class TeamMember(UserContent):
    name = models.CharField(max_length=100)
    photo = models.ImageField()
    display_order = models.IntegerField()

    slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name


class Article(UserContent):
    title = models.TextField()
    teaser = models.CharField(blank=True, null=True, max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    headline_image = models.ImageField(blank=True, null=True)

    slug = models.SlugField(null=False, unique=True)

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("cms:article_detail", kwargs={"slug": self.slug})


class Testimonials(UserContent, SingletonModel):
    class Meta:
        verbose_name = "Testimonials"
        verbose_name_plural = "Testimonials"


class Settings(models.Model):
    dest_dir = models.CharField(
        max_length=255, help_text="Default directory for exported articles."
    )
    site_name = models.CharField(max_length=255, default="", help_text="Site name")
    site_headline = models.CharField(max_length=255, default="", help_text="Site headline")
    site_teaser = models.CharField(max_length=255, default="", help_text="Site teaser")
    about = QuillField()

    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    def clean(self):
        # Ensure only one instance exists
        if Settings.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one instance of 'Settings' is allowed.")

    def save(self, *args, **kwargs):
        # Run clean method before saving
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Settings (dest_dir={self.dest_dir})"
