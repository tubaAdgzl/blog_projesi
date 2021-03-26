from django.urls import reverse
from django.db import models
from django.utils.text import slugify

class Post(models.Model):
    title = models.CharField(max_length=250,verbose_name="Başlık")
    content =models.TextField(verbose_name="İçerik")
    date = models.DateTimeField(auto_now_add=True,verbose_name="Yayın Tarihi")
    slug = models.SlugField(unique=True,editable=False)
    image = models.ImageField(blank=False,null=False,verbose_name="Resim")
    author = models.ForeignKey("auth.user", verbose_name="Yazar", on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail',kwargs={'slug':self.slug})

    def get_unique_slug(self):
        slug = slugify(self.title.replace("ı","i"))
        unique_slug = slug
        counter = 1
        while Post.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug,counter)
            counter += 1
        return unique_slug

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug()
        return super(Post,self).save(*args,**kwargs)

    class Meta:
        ordering = ["-date","id"]

    
class Comment(models.Model):

    post=models.ForeignKey("post.Post",related_name="comments",on_delete=models.CASCADE)
    name = models.CharField(max_length=200, verbose_name="İsim")
    content = models.TextField(max_length=500,verbose_name="Yorum")
    created_date=models.DateTimeField(auto_now_add=True)