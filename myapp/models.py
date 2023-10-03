from django.db import models
from django.utils import timezone
from django.urls import reverse
# Create your models here.
class Post(models.Model):
  title = models.CharField(max_length = 200)
  description = models.TextField(null = True, blank = True)
  image = models.FileField(null = True,blank=True)
  slug = models.SlugField(
    max_length=200,
    unique_for_date="publish",
    default="",
    )
  publish = models.DateTimeField(default=timezone.now)
  def get_absolute_url(self):
    return reverse("myapp:post_comment",
          args = [
              self.publish.year,
              self.publish.month,
              self.publish.day,
              self.slug,
            ]
        )
  def get_delete_post_url(self):
    return reverse("myapp:delete_post",
        args = [
            self.publish.month,
            self.slug,
          ]
    )
  def edit_post_url(self):
    return reverse("myapp:edit_post",
        args = [
            self.publish.day,
            self.slug,
            
          ]
      )
  class Meta:
    ordering = ("-publish",)
  def __str__(self):
    return self.title
    
class Comment(models.Model):
  post = models.ForeignKey(Post,
      on_delete = models.CASCADE,
      max_length = 200,
      related_name = "posts",
  )
  name = models.CharField(max_length=200)
  body = models.TextField()
  publish = models.DateTimeField(default=timezone.now)
  active = models.BooleanField(default=True)
  class Meta:
    ordering = ("-publish",)
  def __str__(self):
    return self.name