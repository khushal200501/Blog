from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Post(models.Model):
    sno = models.AutoField(primary_key=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') 
    title = models.CharField(max_length=200)
    content = models.TextField()
    slug = models.CharField(max_length=200, unique=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + ' by ' + self.user.username

    def number_of_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-timestamp']
            
class BlogComment(models.Model):
    sno=models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp=models.DateTimeField(default=now)

    def __str__(self):
        return "Comment by " + self.user.username + " on Post " + self.post.title



    
