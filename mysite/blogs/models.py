from django.db import models

# Create your models here.


class Blogpost(models.Model):
    blog_title = models.CharField(max_length=200)
    blog_content = models.TextField()
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.blog_title


class Comment(models.Model):
    blogpost = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    def __str__(self):
        return self.comment