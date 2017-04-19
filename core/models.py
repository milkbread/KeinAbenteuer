from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Article(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


def get_image_filename(instance, filename):
    title = instance.article.title
    slug = slugify(title)
    return "posted_images/%s-%s" % (slug, filename)  


class Image(models.Model):
    article = models.ForeignKey(Article, default=None, related_name="images")
    image = models.ImageField(upload_to=get_image_filename,
                              verbose_name='Image', )
