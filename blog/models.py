from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse


category=[("wordpress","Wordpress"),("html","HTML"),
        ("photography","Photography"),("ui","UI"),
        ("mockups","Mockups"),("branding","Branding")]
category_=category

class Post(models.Model):
    category=models.CharField(choices=category,default="wordpress",max_length=20)
    title=models.CharField(max_length=200)
    content=models.TextField()
    date_posted=models.DateField(default=timezone.now)
    author=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="post-images")
    def __str__(self):
         return self.title

    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})

    def get_category(self):
        for key,value in category_:
            if key==self.category:
                return value



class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    author_name=models.CharField(max_length=200)
    author_email=models.EmailField()
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.author_name

class Like(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.post.title