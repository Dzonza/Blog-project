from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.caption}'
    
class Post(models.Model):
    title = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images')
    slug = models.SlugField(unique=True, db_index=True,null=True, blank=True)
    author = models.ForeignKey(User,  on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} {self.author}'
    
    def save(self, *args, **kwargs):
        if not self.slug or self.title != Post.objects.filter(pk=self.pk).first().title:
            self.slug = slugify(self.title)
            unique_slug = self.slug
            num = 1
            while Post.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(self.slug, num)
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)
    
    class Meta:
        app_label ='blog'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images', default='default.png')